from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, UpdateView,
    DeleteView
)


from app.models import DocumentFileType


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filetypes = DocumentFileType.objects.all()
        context['types'] = filetypes
        return context

class FileTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
        model = DocumentFileType
        template_name = 'add_file.html'
        fields = ['file_type', 'file_description']
        success_message = 'Updated successfully'
        success_url = reverse_lazy('list_file_types')


        def test_func(self):

            if self.request.user.has_perm('app.can_register_batch'):
                return True
            return False

class FileTypeDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
        model = DocumentFileType
        success_message = 'Updated successfully'
        success_url = reverse_lazy('list_file_types')
        template_name = 'batch/delete_confirm.html'

        def test_func(self):

            if self.request.user.has_perm('app.can_register_batch'):
                return True
            return False

