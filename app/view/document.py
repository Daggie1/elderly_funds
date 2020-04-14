from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView
from django.utils import timezone
from app.forms import DocumentDetailForm, DocumentBarCodeFormSet, DocFormset
from app.models import DocumentFileDetail, DocumentFile


class DocumentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documentfiledetails'
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
            if documents.is_valid():
                documents.save()
        return super(DocumentCreate, self).form_valid(form)

    def form_invalid(self, form):
        print(form)


class DocumentView(LoginRequiredMixin, ListView):
    permission_required = 'app.add_documentfiledetails'
    template_name = 'app/document/index.html'

    def get_queryset(self):
        return DocumentFileDetail.objects.filter(file_reference_id=self.kwargs['file_ref_no'])

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


def create_document(request, file_ref_no):
    template_name = 'app/document/create.html'
    heading_message = 'Create Document'
    if request.method == 'GET':
        formset = DocFormset(request.GET or None)
    elif request.method == 'POST':
        formset = DocFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                file_reference = DocumentFile.objects.get(pk=file_ref_no)
                document_barcode = form.cleaned_data.get('document_barcode')
                if document_barcode:
                    DocumentFileDetail(document_barcode = document_barcode, file_reference=file_reference, state_id='300', doc_created_by=request.user, created_on=timezone.now()).save()
            return redirect('list_file_types')
    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })

# TODO Restrict characters in File Reference or Deal With Special Characters
# TODO Show update Files, Validate Files Before Mapping