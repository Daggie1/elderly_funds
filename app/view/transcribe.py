from django.core.serializers import json
from django.shortcuts import render
from django.http import JsonResponse

from app.models import Filer, DocumentFile, DocumentFileDetail, DocumentType


def map_keys_to_value_digital(dict_list):
    selectors = []
    for item in dict_list:
        value = item['id']
        label = item['document_barcode']
        dict = {'value': value, 'label': label}
        selectors.append(dict)
    return selectors

def get_files_from_storage(request, file_reference):
    scanned_documents = Filer.objects.filter(file_reference=file_reference).values('filepond', 'file_reference')

    digital_documents = DocumentFileDetail.objects.filter(file_reference=file_reference).values()
    document_type = DocumentType.objects.all().values('document_name')
    file = DocumentFile.objects.get(pk=file_reference)

    context = {'scanned_documents': list(scanned_documents),
               'digital_documents': map_keys_to_value_digital(digital_documents), 'file': file, 'document_type':document_type}

    return render(request, 'transcribe_document.html', context=context)


def update_document_file_detail(request, document):
    # get the document
    document = DocumentFileDetail.objects.get(pk=document)

    document.filepond = request.POST.get('document_path')
    # update the document path and document type
    document.save()
    # return results
    results = {'success': True}
    return JsonResponse(results)

# The next stage will be handled by the existing transcribe document function
# in views.py
