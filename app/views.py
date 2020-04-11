from django.shortcuts import render, redirect, get_object_or_404
from .mixin import FirstTimeLoginMixing
from django.contrib import messages
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .forms import FileForm, DocumentTypeForm, FileContentForm, LoginForm, UserRegistrationForm, \
    PasswordResetForm, GroupCreationForm, BatchCreationForm, DocumentDetailForm, DocumentBarCodeFormSet
from .models import DocumentFile, DocumentFileType, DocumentType, DocumentFileDetail, Batch, DocumentState
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .tables import DocumentFileTable, DocumentTable
from .filters import DocumentFileFilter
from django.contrib.messages.views import SuccessMessageMixin
from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from django_jsonforms.forms import JSONSchemaField, JSONSchemaForm

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .decorators import unauthenticated_user, first_time_login

from django.db.models import Q
from django.shortcuts import render_to_response

from json2html import *

from django.db import transaction


# Create your view here.
def search_file(request):
    pass


def search_person(request):
    query = request.GET.get('q')
    if query:
        qset = (
            Q(title__icontains=query)
        )
        results = DocumentFileDetail.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("search_html", {"results": results, "query": query})


@login_required
def edit_file(request, file_type):
    if file_type:
        file = get_object_or_404(DocumentFileType, pk=file_type)

        return render(request, 'view_document_files.html', {'file': file})


@login_required
def manage_documents(request, file_type):
    if file_type:
        file = get_object_or_404(DocumentFileType, pk=file_type)
        documents = DocumentFile.objects.filter(file_type=file_type)
        form = None
        # form = DOcumentForm()
        context = {'file': file, 'documents': documents, 'form': form}
        return render(request, 'upload_document.html', context)


class AdminView(LoginRequiredMixin, View):
    template_name = 'home.html'

    permission_required = ''

    def get(self, request):
        return render(request, self.template_name)


class BatchListView(LoginRequiredMixin, ListView):
    permission_required = 'app.view_batch'
    model = Batch
    template_name = 'app/batch/index.html'


@login_required
def create_batch(request):
    form = BatchCreationForm(data=request.POST)
    if form.is_valid():
        form.save()
        batch = Batch.objects.get(batch_no=form.cleaned_data.get('batch_no'))
        batch.refresh_from_db()
        batch.created_by = request.user
        batch.save()
        print('iooio')
        messages.success(request, f"Created successfully")
        for batch in Batch.objects.all():
            print(f'batch: {batch.batch_no} name:{batch.name} by:{batch.created_by}')
        return redirect('batch.index')

    else:
        form = BatchCreationForm()
    return render(request, 'app/batch/create.html', {'form': form})


class FileTypeList(LoginRequiredMixin, ListView):
    permission_required = 'app.view_documentfiletype'
    model = DocumentFileType
    template_name = 'file_types.html'
    context_object_name = 'files'


class FileTypeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documentfiletype'
    model = DocumentFileType
    template_name = 'add_file.html'
    fields = ['file_type', 'file_description']
    success_message = 'Added created successfully'
    success_url = reverse_lazy('list_file_types')


class FileTypeDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'app.delete_documentfiletype'
    model = DocumentFileType
    success_message = 'Deleted created successfully'
    success_url = reverse_lazy('list_file_types')

    def test_func(self):
        if self.request.user.profile.first_login:
            return False
        else:
            return True

    class FilesView(LoginRequiredMixin, ListView):

        permission_required = 'app.add_documentfile'
        template_name = 'app/file/index.html'

        def get_queryset(self):
            return DocumentFile.objects.filter(batch=Batch.objects.get(pk=self.kwargs['batch_id']))


class DocumentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documentfiledetails'
    model = DocumentFileDetail
    form_class = DocumentDetailForm
    template_name = 'app/document/create.html'
    success_message = 'Added created successfully'
    success_url = reverse_lazy('list_file_types')


    def get_context_data(self, **kwargs):
        context = super(DocumentCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DocumentBarCodeFormSet(self.request.POST)
        else:
            context['formset'] = DocumentBarCodeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        documents = context['formset']
        with transaction.atomic():
            form.instance.doc_created_by = self.request.user
            form.instance.file_reference = DocumentFile.objects.get(file_reference=self.kwargs['file_ref_no'])
            # self.object = form.save()
            if documents.is_valid():
                documents.save()
        return super(DocumentCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form)


class DocumentView(LoginRequiredMixin, ListView):
    permission_required = 'app.add_documentfiledetails'
    template_name = 'app/document/index.html'

    def get_queryset(self):
        return DocumentFileDetail.objects.filter(file_reference=DocumentFile.objects.get(pk=self.kwargs['file_ref_no']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file_ref_no'] = self.kwargs['file_ref_no']
        return context


class DocumentFileCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documentfile'
    success_message = 'Added created successfully'
    model = DocumentFile
    template_name = 'app/file/create.html'
    fields = ['file_reference', 'file_type', 'file_barcode']
    success_url = reverse_lazy('list_document_files')
    m = None

    def get(self, request, batch_id):
        # query documents belonging to this file & aggregate with its corresponding document type
        DocumentFileCreate.m = batch_id
        print(DocumentFileCreate.m)
        return super().get(request)

    def form_valid(self, form):
        form.instance.file_created_by = self.request.user
        form.instance.batch = Batch.objects.get(pk=DocumentFileCreate.m)
        return super().form_valid(form)


class FilesView(LoginRequiredMixin, ListView):
    permission_required = 'app.add_documentfile'

    def get(self, request, *args, **kwargs):
        batch_id = kwargs['batch_id']
        files = DocumentFile.objects.filter(batch=Batch.objects.get(pk=batch_id))

        return render(request, 'app/file/index.html', {
            'object_list': files,
            'batch_id': batch_id
        })


class DocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'
    model = DocumentFile
    table_class = DocumentFileTable
    template_name = 'view_document_files.html'

    filterset_class = DocumentFileFilter


class DocumentTypeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documenttype'
    model = DocumentType
    success_message = 'Added created successfully'
    template_name = 'add_document_type.html'
    fields = ['document_name', 'document_description', 'document_field_specs']
    success_url = reverse_lazy('list_document_types')


class DocumentTypeList(LoginRequiredMixin, ListView):
    permission_required = 'app.view_documenttype'
    model = DocumentType
    context_object_name = 'documents'
    template_name = 'document_types.html'


class DocumentTypeView(LoginRequiredMixin, SuccessMessageMixin, View):
    permission_required = 'app.view_documenttype'
    success_message = 'Added created successfully'

    def get(self, request):
        template_name = 'add_document_type.html'
        form = DocumentTypeForm()
        return render(request, template_name, {'form': form})

    def post(self, request):
        pass


class DocumentUploadView(LoginRequiredMixin, CreateView):
    permission_required = 'app.add_documentfiledetail'
    model = DocumentFileDetail
    template_name = 'upload_document.html'
    fields = ['file_reference', 'document_barcode', 'document_name', 'document_file_path']
    success_url = reverse_lazy('uploaded_documents')


class UploadedDocumentsList(LoginRequiredMixin, ListView):
    permission_required = 'app.view_documentfiledetail'
    model = DocumentFileDetail
    template_name = 'uploaded_documents_list.html'


class DocumentTranscribe(LoginRequiredMixin, View):
    permission_required = 'app.add_documentfiledetail'

    def get(self, request, file_reference):
        # query documents belonging to this file & aggregate with its corresponding document type
        queryset = DocumentFileDetail.objects.filter(file_reference_id=file_reference)
        print(queryset)
        # file = get_object_or_404(DocumentFile, pk=file_reference)
        table = DocumentTable(queryset)
        return render(request, 'file_documents_list.html', {'table': table})


@login_required
def get_document_and_document_type(request, doc_id, file_type):
    document = get_object_or_404(DocumentFileDetail, pk=doc_id)
    document_type = DocumentType.objects.get(pk=file_type)
    form = JSONSchemaForm(schema=document_type.document_field_specs, options={"theme": "bootstrap3"})
    return render(request, 'transcription_lab.html', {'form': form, 'document': document})

def get_document_list(request, file_reference):
    documents = DocumentFileDetail.objects.filter(file_reference = file_reference);

    return render(request, 'files_list.html', {'documents':documents})

@login_required
def update_document_content(request, doc_id):
    document = DocumentFileDetail.objects.get(id=doc_id)
    document.document_content = request.POST.get('json')
    document.save()
    return redirect('view_docs_in_file', document.file_reference_id)


@login_required
def validate_document_content(request, doc_id):
    document = DocumentFileDetail.objects.get(id=doc_id)
    content = document.document_content
    table_data = json2html.convert(json=content, table_attributes="id=\"info-table\" class=\"table table-bordered "
                                                                  "table-hover\"")
    return render(request, 'validate.html', {'table_data': table_data, 'document': document})


@login_required
def pdfrender(request):
    return render(request, template_name='app/pdfrender.html')


@unauthenticated_user
def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            uname = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=uname, password=pwd)
            if user is not None:
                auth_login(request, user)

                return redirect('users.index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            u = request.user
            print(u)
            u.refresh_from_db()
            u.profile.first_Login = False
            u.save()
            logout(request)
            return redirect('login')
    else:
        form = PasswordResetForm(user=request.user)
    return render(request, 'reset_password.html', {'form': form, })


@login_required
def add_group(request):
    form = GroupCreationForm(request.POST)
    if form.is_valid():
        form.save()

        messages.success(request, f"Group Created successfully")
        return redirect('groups.index')

    else:
        form = GroupCreationForm()
    return render(request, 'create_group.html', {'form': form})


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users.html'


class UserDetailView(LoginRequiredMixin, DetailView):
    permission_required = 'auth.view_user'

    model = User
    template_name = 'user_details.html'


class GroupListView(LoginRequiredMixin, ListView):
    permission_required = 'auth.view_user'

    model = Group
    template_name = 'groups.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    permission_required = 'auth.change_user'

    model = User
    success_url = '/users/'

    fields = ['username', 'email', 'groups', 'is_superuser']
    template_name = 'edit_user.html'


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    permission_required = 'auth.change_group'

    model = Group
    success_url = '/roles/'

    fields = ['name', 'permissions']
    template_name = 'multi_auth/groups/create.html'


class UserDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = 'auth.delete_user'

    model = User
    success_url = '/users/'
    template_name = ''


@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            id_no = form.cleaned_data.get('id_no')
            email = form.cleaned_data.get('email')
            username = id_no
            password = id_no
            groups = form.cleaned_data.get('groups')
            is_superuser = request.POST.get('is_superuser')
            user = None
            if is_superuser:

                user = User.objects.create_superuser(username, email, password)
            else:
                user = User.objects.create_user(username, email, password)
                user.groups.set(groups)
            user.refresh_from_db()
            user.profile.id_no = form.cleaned_data.get('id_no')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.save()
            messages.success(request, f'User created successfully!')
            return redirect('users.index')

    else:
        form = UserRegistrationForm()
    return render(request, 'create_user.html', {
        'groups': Group.objects.all(),
        'form': form,
    })


@login_required
def group_create(request):
    return render(request, 'create_group.html')


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group

    permission_required = 'auth.view_group'
    permissions = Permission.objects.all()
    extra_context = permissions
    template_name = 'create_group.html'
    fields = ['name', 'permission']
    success_url = 'home'


def registry_submit(request, batch_id):
    batch = Batch.objects.get(pk=batch_id)
    print(batch)
    batch.state = DocumentState.objects.get(state_code=301)
    batch.save()
    messages.success(request, 'Submitted successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
