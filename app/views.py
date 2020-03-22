from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .forms import FileForm, DocumentTypeForm, DocumentForm, FileContentForm, LoginForm, UserRegistrationForm, \
    PasswordResetForm, GroupCreationForm
from .models import DocumentFile, DocumentFileType, DocumentType, DocumentFileDetail
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .tables import DocumentFileTable, DocumentTable
from .filters import DocumentFileFilter
from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from django_jsonforms.forms import JSONSchemaField, JSONSchemaForm

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from .decorators import unauthenticated_user

from django.db.models import Q
from django.shortcuts import render_to_response

from json2html import *


# Create your views here.
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


def edit_file(request, file_type):
    if file_type:
        file = get_object_or_404(DocumentFileType, pk=file_type)
        return render(request, 'view_document_files.html', {'file': file})


def manage_documents(request, file_type):
    if file_type:
        file = get_object_or_404(DocumentFileType, pk=file_type)
        documents = DocumentFile.objects.filter(file_type=file_type)
        form = DocumentForm()
        context = {'file': file, 'documents': documents, 'form': form}
        return render(request, 'upload_document.html', context)


def add_document(request, file_type):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = DocumentForm(docfile=request.FILES['document'])
            newdoc.save()

            return HttpResponseRedirect(reverse('upload'))
        else:
            form = DocumentForm()

    form = DocumentForm()
    documents = Document.objects.all()
    return render(request, 'list.html', {'documents': documents, 'form': form})


class AdminView(LoginRequiredMixin, View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class FileTypeList(ListView):
    model = DocumentFileType
    template_name = 'file_types.html'
    context_object_name = 'files'


class FileTypeCreate(CreateView):
    model = DocumentFileType
    template_name = 'add_file.html'
    fields = ['file_type', 'file_description']
    success_url = reverse_lazy('list_file_types')


class FileTypeDelete(DeleteView):
    model = DocumentFileType

    success_url = reverse_lazy('list_file_types')


class DocumentFileCreate(CreateView):
    model = DocumentFile
    template_name = 'create_document_file.html'
    fields = ['file_reference', 'file_type', 'file_barcode']
    success_url = reverse_lazy('list_document_files')


class DocumentFileList(SingleTableMixin, FilterView):
    model = DocumentFile
    table_class = DocumentFileTable
    template_name = 'view_document_files.html'

    filterset_class = DocumentFileFilter


class DocumentTypeCreate(CreateView):
    model = DocumentType
    template_name = 'add_document_type.html'
    fields = ['document_name', 'document_description', 'document_field_specs']

    success_url = reverse_lazy('list_document_types')


class DocumentTypeList(ListView):
    model = DocumentType
    context_object_name = 'documents'
    template_name = 'document_types.html'


class DocumentTypeView(View):
    def get(self, request):
        template_name = 'add_document_type.html'
        form = DocumentTypeForm()
        return render(request, template_name, {'form': form})

    def post(self, request):
        pass


class DocumentUploadView(CreateView):
    model = DocumentFileDetail
    template_name = 'upload_document.html'
    fields = ['file_reference', 'document_barcode', 'document_name', 'document_file_path']
    success_url = reverse_lazy('uploaded_documents')


class UploadedDocumentsList(ListView):
    model = DocumentFileDetail
    template_name = 'uploaded_documents_list.html'


class DocumentTranscribe(View):
    def get(self, request, file_reference):
        # query documents belonging to this file & aggregate with its corresponding document type
        queryset = DocumentFileDetail.objects.filter(file_reference_id=file_reference)
        print(queryset)
        # file = get_object_or_404(DocumentFile, pk=file_reference)
        table = DocumentTable(queryset)
        return render(request, 'file_documents_list.html', {'table': table})


def get_document_and_document_type(request, doc_id, file_type):
    document = get_object_or_404(DocumentFileDetail, pk=doc_id)
    document_type = DocumentType.objects.get(pk=file_type)
    form = JSONSchemaForm(schema=document_type.document_field_specs, options={"theme": "bootstrap3"})
    return render(request, 'transcription_lab.html', {'form': form, 'document': document})


def update_document_content(request, doc_id):
    document = DocumentFileDetail.objects.get(id=doc_id)
    document.document_content = request.POST.get('json')
    document.save()
    return redirect('view_docs_in_file', document.file_reference_id)


def validate_document_content(request, doc_id):
    document = DocumentFileDetail.objects.get(id=doc_id)
    content = document.document_content
    table_data = json2html.convert(json=content, table_attributes="id=\"info-table\" class=\"table table-bordered "
                                                                  "table-hover\"")
    return render(request, 'validate.html', {'table_data': table_data, 'document': document})


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
                if request.user.profile.first_login:
                    return redirect('user.changepass')
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
            u.profile.first_Login = False
            u.save()
            logout(request)
            return redirect('login')
    else:
        form = PasswordResetForm(user=request.user)
    return render(request, 'reset_password.html', {'form': form, })


@login_required
@permission_required('auth.add_group', raise_exception=True)
def add_group(request):
    form = GroupCreationForm(request.POST)
    if form.is_valid():
        form.save()

        messages.success(request, f"Group Created successfully")
        return redirect('groups.index')

    else:
        form = GroupCreationForm()
    return render(request, 'create_group.html', {'form': form})


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    raise_exception = True
    permission_required = 'auth.view_user'
    model = User
    template_name = 'users.html'


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    # print(f"from detail"+s['ph'])
    permission_required = 'auth.view_user'
    raise_exception = True
    model = User
    template_name = 'user_details.html'


class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'auth.view_user'
    raise_exception = True
    model = Group
    template_name = 'groups.html'


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_user'
    raise_exception = True
    model = User
    success_url = '/users/'

    fields = ['username', 'email', 'groups', 'is_superuser']
    template_name = 'edit_user.html'


class GroupUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_group'
    raise_exception = True
    model = Group
    success_url = '/roles/'

    fields = ['name', 'permissions']
    template_name = 'multi_auth/groups/create.html'


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'auth.delete_user'
    raise_exception = True
    model = User
    success_url = '/users/'
    template_name = ''


@login_required
def index(request):
    context = {
        'title': 'Admin Dashboard',
        'subtitle': 'Dashboard',
        'current_url': 'Dashboard'
    }

    # s=SessionStore()
    # s['ph']=request.session['phone']
    # s.create()
    # print(s['ph'])

    return render(request, 'multi_auth/index.html', context)


@login_required
@permission_required('auth.add_user', raise_exception=True)
def user_create(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            id_no = request.POST.get('id_no')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            groups = form.cleaned_data.get('groups')
            is_superuser = request.POST.get('set_super_admin')

            if is_superuser == 'on':

                User.objects.create_superuser(username, email, id_no)
            else:
                user = User.objects.create_user(username, email, id_no)
                user.groups.set(groups)
            messages.success(request, f'User created successfully!')
            return redirect('users.index')

    else:
        form = UserRegistrationForm()
    return render(request, 'create_user.html', {
        'groups': Group.objects.all(),
        'form': form,
    })


@login_required
@permission_required('auth.add_group', raise_exception=True)
def group_create(request):
    return render(request, 'create_group.html')


class GroupCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Group

    raise_exception = True
    permission_required = 'auth.view_group'
    permissions = Permission.objects.all()
    extra_context = permissions
    template_name = 'create_group.html'
    fields = ['name', 'permission']
    success_url = 'home'
