from django.db.models import Q
from django.shortcuts import render
import itertools

from app.models import DocumentFileDetail, DocumentFile, Batch


def receive(request,id=None):
    # make a query
    # documents = DocumentFileDetail.objects.get(pk=id)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        query = request.GET.get('q')
        if query:
            qset = (
                Q(file_barcode__icontains=query)
            )
            results = Batch.objects.filter(qset).distinct()
        else:
            results = []
        if id is not None:
            files = DocumentFile.objects.filter(file_reference=id).values_list('document_barcode', flat=True)
            batch = Batch.objects.get(pk=id)
        else:
            batch = ''
            files = []
    context = {'results': results, 'batch':batch,'files':list(files)}
    return render(request, 'inspect/receiver.html',context=context)


def inspect(request, id=None):
    # make a query
    # documents = DocumentFileDetail.objects.get(pk=id)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        query = request.GET.get('q')
        if query:
            qset = (
                Q(file_barcode__icontains=query)
            )
            results = DocumentFile.objects.filter(qset).distinct()
        else:
            results = []
        if id is not None:
            documents = DocumentFileDetail.objects.filter(file_reference=id).values_list('document_barcode', flat=True)
            file = DocumentFile.objects.get(pk=id)
        else:
            file = ''
            documents = []
    context = {'results': results, 'file': file, 'documents': list(documents)}
    print(documents)
    return render(request, 'inspect/index.html', context=context)
