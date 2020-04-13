from django.shortcuts import redirect


class LoggedInRedirectMixin:

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('users.index')
        else:
            return super().dispatch(request, *args, **kwargs)
