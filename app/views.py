from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.views import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView

from django.contrib.auth.models import Group, User, Permission
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .mixin import LoggedInRedirectMixin

from django.urls import reverse_lazy,reverse
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



class Login(LoggedInRedirectMixin, LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        print(form.get_user())
        # form is valid (= correct password), now check if user requires to set own password
        if form.get_user().profile.first_login:

            return redirect(reverse_lazy('user.changepass', kwargs={'username': form.get_user().username}))
        else:
            auth_login(self.request, form.get_user())
            return redirect(self.get_success_url())

def change_password(request, username):
    user = User.objects.get(username=username)
    print(f'user{user.password}')

    if request.method == 'POST':
        #user=authenticate(username=user.username, password=request.POST.get('old_password'))
        print(user)
        form = PasswordChangeForm(data=request.POST, user=user)

        if form.is_valid():

            form.save()
            user.refresh_from_db()
            user.profile.first_login = False
            user.save()
            messages.success(request, 'Password Changed Successfully,')
            return redirect(reverse('login'))
        else:
            messages.error(request, form.error_messages)
            return redirect(reverse('user.changepass', kwargs={'username': user.username}))
    else:
        form = PasswordChangeForm(user=user)

        args = {'form': form}
        return render(request, 'reset_password.html', args)



@login_required
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(user=request.user, data=request.POST)

        if form.is_valid():

            form.save()
            u = user
            print(u)
            u.refresh_from_db()
            u.profile.first_Login = False
            u.save()
            logout(request)
            return redirect('login')
        else:
           print(form.error_messages)
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



#receive and registry
@login_required
def batch_submit(request, batch_id):
    batch = Batch.objects.get(pk=batch_id)
    if batch.state.state_code <=301:
        if batch and not request.user.has_perm(batch.state.permission):

            try:

                files = DocumentFile.objects.filter(batch=batch)
                docs = DocumentFileDetail.objects.filter(file_reference__in=files)

                if files and docs:
                    new_state=None
                    desc=None
                    current_state=DocumentState.objects.get(state_code=int(batch.state.state_code))
                    if request.POST.get('reject_check')=='on':
                        new_state=current_state+100
                        desc=request.POST.get('idesc')

                    else:
                        new_state = current_state+1
                    if current_state==300:
                        docs.update(state=new_state, )
                        files.update(state=new_state)
                        batch.state = new_state
                        batch.rejection_by_receiver_dec=desc
                        batch.save()
                    elif current_state==301 and not batch.received_by:
                        docs.update(state=new_state, )
                        files.update(state=new_state)
                        batch.state = new_state
                        batch.received_on = timezone.now()
                        batch.save()
                        messages.success(request, 'Submitted successfully')
                else:

                    messages.error(request, 'Empty batch or file')
            except AttributeError as e:
                messages.error(request, ' something wrong happened')
        else:
            return redirect('abort')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def file_or_files(request,file_ref=None,**kwargs):

    if not file_ref==None:
        file = DocumentFile.objects.get(file_reference=file_ref)

        if file and request.user.has_perm(file.state.permission):
            return file
    if kwargs.get('batch',False):
        return DocumentFile.objects.filter(batch=kwargs['batch'])


def doc_or_docs(request, file):

        return DocumentFileDetail.objects.filter(file_reference=file)

@login_required
def request_file(request):
    state = DocumentState.objects.get(state_code=303)
    if request.user.has_perm(state.permission):

        file = DocumentFile.objects.filter(state=state, file_transcribed_by=None).first()
        if file:
            try:
                file.file_transcribed_by = request.user
                file.save()
                messages.success(request, 'New File Given')

            except AttributeError as e:
                messages.error(request, ' something wrong happened')
        else:
            messages.warning(request, 'No files Available')
    messages.error(request, ' something wrong happened')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def abort(request):
    return render(request, 'app/others/lock_screen.html')
def file_submit(request, file_ref):
    file=file_or_files(request,file_ref)
    print(file)
    docs=doc_or_docs(request,file)
    print(docs)
    desc=None
    if request.POST.get('reject_check')=='on':
       desc=request.POST.get('desc')
    change_state(request, file,docs,False,desc)
    messages.success(request,'Updated Successfull')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def change_state(request ,file=None,docs=None,is_reject=None,desc=None):
    file= file
    docs=docs

    if file and docs:
        curren_state=int(file.state.state_code)
        desc=None
        new_state=None
        print(f'changes {file.state.state_code} and {docs}')
        if  is_reject:
            new_state = DocumentState.objects.get(state_code=int(file.state.state_code) + 100)
            desc=desc
        else:
            new_state = DocumentState.objects.get(state_code=int(file.state.state_code) + 1)

        if curren_state == 302:

            docs.update(state=new_state,
                        scanned_on=timezone.now()
                        )
            file.state=new_state
            file. file_scanned_by=request.user
            file.scanned_on=timezone.now()
            file.save()
        elif curren_state == 303:
            docs.update(state=new_state,
                        transcribed_on=timezone.now(),
                        rejection_by_transcriber_dec=desc
                        )
            file.state=new_state
            file.transcribed_by=request.user
            file.transcribed_on=timezone.now()
            file.rejection_by_transcriber_dec = desc
            file.save()

        elif curren_state == 304:
            docs.update(state=new_state,
                        qa_on=timezone.now(),
                        rejection_by_qa_dec=desc
                        )
            file.state=new_state
            file.file_qa_by=request.user
            file.qa_on=timezone.now()
            file.rejection_by_qa_dec = desc
            file.save()
        elif curren_state == 305:
            docs.update(state=new_state,
                        validated_on=timezone.now(),
                        rejection_by_validation_dec=desc
                        )
            file.state=new_state
            file.file_validated_by=request.user
            file.validated_on=timezone.now()
            
            file.rejection_by_validation_dec = desc
            file.save()
def start_receive(request,batch_id):
    batch=Batch.objects.get(pk=batch_id)
    if batch and not batch.received_by:
        batch.received_by=request.user
        batch.save()
        #return receive page
def start_scanning(request,file_ref):
    file = file_or_files(request, file_ref)
    if file and file.state.state_code ==303 and not file.file_scanned_by:
        docs = doc_or_docs(request, file)
        try:
            docs.update(
                doc_scanned_by=request.user
            )

            file.file_scanned_by=request.user
        except AttributeError as e:
            messages.error(request, ' something wrong happened')
    # return to scanning page
    else:
        messages.error(request, ' something wrong happened')



def start_qa(request, file_ref):
    file = file_or_files(request, file_ref)
    if file and file.state.state_code ==304 and not file.file_qa_by :
        docs = doc_or_docs(request, file)
        try:
            docs.update(
                doc_qa_by=request.user
            )


            file.file_qa_by = request.user
        except AttributeError as e:
            messages.error(request, ' something wrong happened')
    # return to scanning page
    else:
        messages.error(request, ' something wrong happened')


def start_validate(request, file_ref):
    file = file_or_files(request, file_ref)
    if file and file.state.state_code ==305 and not file.file_validated_by :
        docs = doc_or_docs(request, file)
        try:
            docs.update(
                doc_qa_by=request.user
            )


            file.file_validated_by = request.user
        except AttributeError as e:
            messages.error(request, ' something wrong happened')
    # return to scanning page
    else:
        messages.error(request, ' something wrong happened')

def registry_submit(request, batch_id):
    batch = Batch.objects.get(pk=batch_id)
    print(batch)
    batch.state = DocumentState.objects.get(state_code=301)
    batch.save()
    messages.success(request, 'Submitted successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
