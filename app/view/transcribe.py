from django.core.serializers import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

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
               'digital_documents': map_keys_to_value_digital(digital_documents), 'file': file,
               'document_type': list(document_type)}

    return render(request, 'transcribe_document.html', context=context)


@csrf_exempt
def update_document_file_detail(request, document):
    # get the document
    # update the document_path, document_type
    print(document)
    if request.POST and document is not None:
        document = get_object_or_404(DocumentFileDetail, pk=document)
        if document is None:
            response = JsonResponse()
            response.status_code = 400
            return response
        document_path = request.POST.get('document_path')
        document_type = request.POST.get('document_type')
        document_type_instance = get_object_or_404(DocumentType, pk=document_type)
        if document_type_instance is None:
            response = JsonResponse()
            response.status_code = 400
            return response
        document.document_type = document_type_instance
        document.document_file_path = document_path
        document.save()
        response = JsonResponse({'success':'update was success'})
        response.status_code = 200
        return response
    else:
        response =  JsonResponse({'error':'update failed'})
        response.status_code  = 500
        return response