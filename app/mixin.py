from django.shortcuts import redirect


class FirstTimeLoginMixing:

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile.first_login:
            return redirect('user.changepass')
        else:
            return super().dispatch(request, *args, **kwargs)