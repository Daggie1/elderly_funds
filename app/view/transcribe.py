from django.core.serializers import json
from django.shortcuts import render

from app.models import Filer, DocumentFile, DocumentFileDetail


def get_files_from_storage(request, file_reference):
    scanned_documents = Filer.objects.filter(file_reference=file_reference).values()

    digital_documents = DocumentFileDetail.objects.filter(file_reference=file_reference).values()

    file = DocumentFile.objects.get(pk=file_reference)

    context = {'scanned_documents': list(scanned_documents), 'digital_documents': list(digital_documents), 'file': file}

    return render(request, 'transcribe_document.html', context=context)


def update_document_file_detail(request):
    # get the document
    # update the document path and document type
    # return results
    pass

# The next stage will be handled by the existing transcribe document function
# in views.py
