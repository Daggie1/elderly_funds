from django.contrib import messages
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.views import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import urllib.parse
from django.contrib.auth.views import LoginView

from django.contrib.auth.models import Group, User, Permission
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableMixin

from .mixin import LoggedInRedirectMixin

from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django_jsonforms.forms import JSONSchemaForm
import urllib
from json2html import *

from django.core import exceptions
from .forms import UserRegistrationForm,GroupCreationForm,UserUpdateForm,ProfileUpdateForm,ElderyRegistrationForm
class Login(LoggedInRedirectMixin, LoginView):
    template_name = 'login.html'
    def form_valid(self, form):
        print(form.get_user())
        # form is valid (= correct password), now check if user requires to set own password
        if form.get_user().profile.first_login:

            return redirect(reverse_lazy('user.changepass', kwargs={'username': form.get_user().username}))


        return super().form_valid(form)

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users.html'

class ElderlyListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'elderly_users.html'
    def get_queryset(self):
        return User.objects.filter(groups__name="elderly",is_superuser=False)
class GuardiansListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'guardians_users.html'
    def get_queryset(self):
        return User.objects.filter(groups__name="guardian",is_superuser=False)

class UserDetailView(LoginRequiredMixin, DetailView):
    permission_required = 'auth.view_user'

    model = User
    template_name = 'user_details.html'
@login_required

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    permission_required = 'auth.change_user'

    model = User
    success_url = '/users/'

    fields = ['username', 'email', 'groups', 'is_superuser']
    template_name = 'edit_user.html'

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
def elderly_create(request):
    if request.method == 'POST':
        form = ElderyRegistrationForm(request.POST)
        if form.is_valid():
            id_no = form.cleaned_data.get('id_no')
            email = form.cleaned_data.get('email')
            username = id_no
            password = id_no
            group=None
            try:
                group = Group.objects.get(name='elderly')
            except Exception  as e:
                messages.error(request, f'group elderly not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = User.objects.create_user(username, email, password)
            user.groups.add(group)
            user.refresh_from_db()
            user.profile.id_no = form.cleaned_data.get('id_no')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.save()
            messages.success(request, f'Elderly created successfully!')
            return redirect('users.create.guardian', user.pk)


    else:
        form = ElderyRegistrationForm()
    return render(request, 'create_user.html', {
        'form': form,
    })
@login_required
def guardian_create(request,elderly_id):
    if request.method == 'POST':
        form = ElderyRegistrationForm(request.POST)
        if form.is_valid():
            id_no = form.cleaned_data.get('id_no')
            email = form.cleaned_data.get('email')
            username = id_no
            password = id_no
            group = None
            try:
                group = Group.objects.get(name='guardian')
            except Exception  as e:
                messages.error(request, f'group elderly not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = User.objects.create_user(username, email, password)
            user.groups.add(group)
            user.refresh_from_db()
            user.profile.id_no = form.cleaned_data.get('id_no')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.elderly_id =elderly_id
            user.save()
            messages.success(request, f'User created successfully!')
            return redirect('users.index')


    else:
        form = ElderyRegistrationForm()
    return render(request, 'create_user.html', {
        'form': form,
    })
class UserDetailView(LoginRequiredMixin, DetailView):
    permission_required = 'auth.view_user'

    model = User
    template_name = 'user_details.html'

def change_password(request, username):
    user = User.objects.get(username=username)
    print(f'user{user.password}')

    if request.method == 'POST':
        # user=authenticate(username=user.username, password=request.POST.get('old_password'))
        print(user)
        form = PasswordChangeForm(data=request.POST, user=user)

        if form.is_valid():

            form.save()
            user.refresh_from_db()
            user.profile.first_login = False
            user.save()
            # update_session_auth_hash(request, form.user)

            messages.success(request, 'Password Changed Successfully, you can now login')
            return redirect(reverse('login'))
        else:
            messages.error(request, form.error_messages)
            return redirect(reverse('user.changepass', kwargs={'username': user.username}))
    else:
        form = PasswordChangeForm(user=user)

        args = {'form': form}
        return render(request, 'reset_password.html', args)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = 'auth.delete_user'

    model = User
    success_url = '/users/'
    template_name = 'user/delete_confirm.html'




    #groups
class GroupListView(LoginRequiredMixin, ListView):
    permission_required = 'auth.view_user'

    model = Group
    template_name = 'groups.html'

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

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    permission_required = 'auth.change_group'

    model = Group
    success_url = '/roles/'

    fields = ['name', 'permissions']
    template_name = 'create_group.html'

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = 'auth.delete_user'

    model = User
    success_url = '/roles/'
    template_name = 'group_delete_confirm.html'

