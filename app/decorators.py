from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users.index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def first_time_login(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.profile.first_login:
            return redirect('user.changepass')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func