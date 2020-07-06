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

def assigned_to_me( original_fuction):
        def wrapper_fuction(*args,**kwargs):
            if args[0].assigned_to == kwargs.get('user') or args[0].assigned_to == None:
                print(f'kwargs={kwargs.get("user")}')
                print(f'args ={args[0].assigned_to }')
                return original_fuction(*args,**kwargs)



        return  wrapper_fuction