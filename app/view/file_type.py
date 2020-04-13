from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

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