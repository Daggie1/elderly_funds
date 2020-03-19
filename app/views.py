from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import DeleteView, CreateView
from django.views.generic import ListView, DetailView
from .forms import FileForm, DocumentTypeForm, DocumentForm, BirthCertificateForm
from .models import DocumentFile, DocumentFileType, DocumentType
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .tables import DocumentFileTable
from .filters import DocumentFileFilter
from django_tables2 import SingleTableView,SingleTableMixin
from django_filters.views import FilterView


# Create your views here.
def search_file(request):
    pass


def edit_file(request, file_type):
    if file_type:
        file = get_object_or_404(DocumentFileType, pk=file_type)
        return render(request, 'view_document_files.html', {'file': file})


def manage_documents(request, file_type):
    if file_type:
        file = get_object_or_404(DocumentFileType, pk=file_type)
        documents = DocumentFile.objects.filter(file_type=file_type)
        form = DocumentForm()
        context = {'file': file, 'documents': documents, 'form': form}
        return render(request, 'upload_document.html', context)


def add_document(request, file_type):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = DocumentForm(docfile=request.FILES['document'])
            newdoc.save()

            return HttpResponseRedirect(reverse('upload'))
        else:
            form = DocumentForm()

    form = DocumentForm()
    documents = Document.objects.all()
    return render(request, 'list.html', {'documents': documents, 'form': form})


class AdminView(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class FileTypeList(ListView):
    model = DocumentFileType
    template_name = 'file_types.html'
    context_object_name = 'files'


class FileTypeCreate(CreateView):
    model = DocumentFileType
    template_name = 'add_file.html'
    fields = ['file_type', 'file_description']
    success_url = reverse_lazy('list_file_types')


class FileTypeDelete(DeleteView):
    model = DocumentFileType

    success_url = reverse_lazy('list_file_types')


class DocumentFileCreate(CreateView):
    model = DocumentFile
    template_name = 'create_document_file.html'
    fields = ['file_reference', 'file_type', 'file_barcode']
    success_url = reverse_lazy('list_document_files')


class DocumentFileList(SingleTableMixin, FilterView):
    model = DocumentFile
    table_class = DocumentFileTable
    template_name = 'view_document_files.html'

    filterset_class = DocumentFileFilter


class DocumentTypeCreate(CreateView):
    model = DocumentType
    template_name = 'add_document_type.html'
    fields = ['document_name','document_description','document_field_specs']

    success_url = reverse_lazy('list_document_types')

class DocumentTypeList(ListView):
    model = DocumentType
    context_object_name = 'documents'
    template_name = 'document_types.html'


class DocumentTypeView(View):
    def get(self, request):
        template_name = 'add_document_type.html'
        form = DocumentTypeForm()
        return render(request, template_name, {'form': form})

    def post(self, request):
        pass


class DocumentUpload(View):
    def get(self, request):
        template_name = 'upload_document.html'
        form = DocumentForm()
        return render(request, template_name, {'form': form})

    def post(self, request):
        template_name = 'upload_document.html'
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                newdoc = DocumentFile(docfile=request.FILES['docfile'])
                newdoc.save()

                return redirect('upload_document')
        form = DocumentForm()
        return render(request, template_name, {'form': form})


class TranscribeDocument(View):
    def get(self, request):
        form = BirthCertificateForm()
        template_name = 'transcribe_document.html'
        return render(request, template_name, {'form': form})
