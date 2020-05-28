"""
Purpose: Upload documents from a physical file to its digital file
Methods: Lookup a file by ref no to upload to, lookup(params: File Reference No)
        Create a folder by the reference no and return the path create_digital_file(reference_no) returns path
        Upload documents to the folder upload(request)
        Delete document from folder delete_document(request)
        Update File state to next stage
"""
import pathlib
import urllib.parse
from django.db.models import Q

from django.http import HttpResponseRedirect
from django.template.defaultfilters import pprint
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django_filters.views import FilterView

from app.views import start_scanning
from app.forms import StorageForm
from app.models import DocumentFile, DocumentFileDetail, Filer,STAGES
from django.shortcuts import render, render_to_response, redirect
from django_tables2 import SingleTableMixin, RequestConfig
from app.tables import ScannerTable
from app.filters import DocumentFileFilter

@csrf_exempt
def upload_documents_to_file(request, file_reference):
    """
    upload the documents from the user
    counter check the number of expected documents
    validate all documents are of pdf type
    """
    file_ref = urllib.parse.unquote(file_reference)
    file = DocumentFile.objects.get(pk=file_ref)
    file_documents  = Filer.objects.filter(file_reference=file_ref)
    form = StorageForm(request.POST, request.FILES)
    if form.is_valid():

        new_file = form.save(commit=False)
        new_file.file_reference = file
        new_file.save()
    else:
        print(form.errors)
    return render(request, 'upload_document.html', {'file': file, 'documents':file_documents})


def delete_document(request, id):
    doc = Filer.objects.get(pk=id)
    doc.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ScannerTableView(SingleTableMixin,FilterView):
    table_class = ScannerTable
    filterset_class = DocumentFileFilter
    model = DocumentFile
    template_name = "files_list.html"

    def get_queryset(self):
        queryset = DocumentFile.objects.filter(stage='Scanner').order_by('-created_on')
        self.table = ScannerTable(queryset)
        self.filter = DocumentFileFilter(self.request.GET,
                                  DocumentFile.objects.filter(stage='Scanner').order_by('-created_on'))
        self.table = ScannerTable(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['table'] = self.table
        context['filter'] = self.filter
        return context

def update_file_state(request, id):
    file = DocumentFile.objects.get(pk=id)
    file.file_status = 'next stage'
    pass
