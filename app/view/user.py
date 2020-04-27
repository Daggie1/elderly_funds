from app.forms import UserUpdateForm,ProfileUpdateForm,ResetPassword
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect,reverse
from django.contrib.auth.models import User
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

@login_required
def admin_check_user(request, pk):
    user=User.objects.get(pk=pk)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_obj':user
    }

    return render(request, 'user/admin_check_userprofile.html', context)
def reset_default_password(request):
    if request.method == 'POST':

        form= ResetPassword(request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            print(username)
            user = User.objects.get(username=username)
            if user:
                try:
                    user.set_password(user.profile.id_no)
                    user.profile.first_login=True
                    user.save()
                    messages.info(request,'use your ID NO as your old password')
                    return redirect(reverse('user.changepass',kwargs={'username':username}))
                except():
                    messages.error(request,'Unable to chnage to default password')
                    pass


    else:
       form=ResetPassword()

    context = {

        'form': form
    }

    return render(request, 'user/reset_password.html', context)
