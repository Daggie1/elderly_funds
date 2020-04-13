from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from app.filters import DocumentFileFilter
from app.models import DocumentFile, Batch
from app.tables import DocumentFileTable


class DocumentFileCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documentfile'
    success_message = 'Added created successfully'
    model = DocumentFile
    template_name = 'app/file/create.html'
    fields = ['file_reference', 'file_type', 'file_barcode']
    success_url = reverse_lazy('list_document_files')
    m = None

    def get(self, request, batch_id):
        # query documents belonging to this file & aggregate with its corresponding document type
        DocumentFileCreate.m = batch_id
        print(DocumentFileCreate.m)
        return super().get(request)

    def form_valid(self, form):
        form.instance.file_created_by = self.request.user
        form.instance.batch = Batch.objects.get(pk=DocumentFileCreate.m)
        return super().form_valid(form)


class FilesView(LoginRequiredMixin, ListView):
    permission_required = 'app.add_documentfile'

    def get(self, request, *args, **kwargs):
        batch_id = kwargs['batch_id']
        files = DocumentFile.objects.filter(batch=Batch.objects.get(pk=batch_id))

        return render(request, 'app/file/index.html', {
            'object_list': files,
            'batch_id': batch_id
        })


class DocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'
    model = DocumentFile
    table_class = DocumentFileTable
    template_name = 'view_document_files.html'

    filterset_class = DocumentFileFilter
