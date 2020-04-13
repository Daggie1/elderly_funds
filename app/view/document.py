from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from app.forms import DocumentDetailForm, DocumentBarCodeFormSet
from app.models import DocumentFileDetail, DocumentFile


class DocumentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documentfiledetails'
    model = DocumentFileDetail
    form_class = DocumentDetailForm
    template_name = 'app/document/create.html'
    success_message = 'Added created successfully'
    success_url = reverse_lazy('list_file_types')

    def get_context_data(self, **kwargs):
        context = super(DocumentCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DocumentBarCodeFormSet(self.request.POST)
        else:
            context['formset'] = DocumentBarCodeFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        documents = context['formset']
        with transaction.atomic():
            form.instance.doc_created_by = self.request.user
            form.instance.file_reference = DocumentFile.objects.get(file_reference=self.kwargs['file_ref_no'])
            # self.object = form.save()
            if documents.is_valid():
                documents.save()
        return super(DocumentCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form)


class DocumentView(LoginRequiredMixin, ListView):
    permission_required = 'app.add_documentfiledetails'
    template_name = 'app/document/index.html'

    def get_queryset(self):
        return DocumentFileDetail.objects.filter(file_reference=DocumentFile.objects.get(pk=self.kwargs['file_ref_no']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file_ref_no'] = self.kwargs['file_ref_no']
        return context


class DocumentUploadView(LoginRequiredMixin, CreateView):
    permission_required = 'app.add_documentfiledetail'
    model = DocumentFileDetail
    template_name = 'upload_document.html'
    fields = ['file_reference', 'document_barcode', 'document_name', 'document_file_path']
    success_url = reverse_lazy('uploaded_documents')


class UploadedDocumentsList(LoginRequiredMixin, ListView):
    permission_required = 'app.view_documentfiledetail'
    model = DocumentFileDetail
    template_name = 'uploaded_documents_list.html'
