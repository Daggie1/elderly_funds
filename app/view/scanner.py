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
from app.models import DocumentFile, DocumentFileDetail, Filer
from django.shortcuts import render, render_to_response, redirect
from django_tables2 import SingleTableMixin
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
    print(file_ref)
    file = DocumentFile.objects.get(pk=file_ref)

    print(file)

    form = StorageForm(request.POST, request.FILES)
    if form.is_valid():

        new_file = form.save(commit=False)
        new_file.file_reference = file
        new_file.save()
    else:
        print(form.errors)

    return render(request, 'upload_document.html', {'file': file})


# def get_file_to_upload_documents(request):
#     if request.method == 'GET':
#         query = request.GET.get('q')
#         if query:
#             qset = (
#                 Q(file_reference_icontains=query)
#             )
#             results = DocumentFile.objects.filter(qset).distinct()
#         else:
#             results = []
#
#     files = DocumentFile.objects.all().order_by('created_on')[:10]
#
#     context = {'files': files, 'results': results}

    # return render(request, 'files_list.html', context=context)

class ScannerTableView(SingleTableMixin,FilterView):
    table_class = ScannerTable
    filterset_class = DocumentFileFilter
    model = DocumentFile
    template_name = "files_list.html"
    

def update_file_state(request, id):
    file = DocumentFile.objects.get(pk=id)
    file.file_status = 'next stage'
    pass
