from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django_jsonforms.forms import JSONSchemaForm
from json2html import *

from .decorators import unauthenticated_user
from .forms import LoginForm, UserRegistrationForm, \
    PasswordResetForm, GroupCreationForm
from .models import DocumentFile, DocumentFileType, DocumentType, DocumentFileDetail, Batch, DocumentState
from .tables import DocumentTable


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
    template_name = 'file/index.html'

    def get_queryset(self):
        return DocumentFile.objects.filter(batch=Batch.objects.get(pk=self.kwargs['batch_id']))


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
    documents = DocumentFileDetail.objects.filter(file_reference=file_reference);

    return render(request, 'files_list.html', {'documents': documents})


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
