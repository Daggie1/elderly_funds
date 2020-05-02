from django.db.models import Q
from django.shortcuts import redirect, reverse


from django.contrib import messages


from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
import itertools

from app.models import DocumentFileDetail, DocumentFile, Batch, Modification


def receive(request,id=None):
    # make a query
    # documents = DocumentFileDetail.objects.get(pk=id)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        query = request.GET.get('q')
        if query:
            qset = (
                Q(batch_no__icontains=query)
            )
            results = Batch.objects.filter(qset).distinct()
        else:
            results = []
        if id is not None:
            files = DocumentFile.objects.filter(batch=id).values('file_barcode','file_reference','state')
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

            if file.assigned_to == None:
                returned_object_type = ContentType.objects.get(app_label='app', model='documentfile')
                print(f'returned_obj={returned_object_type}')
                try:
                    file.assigned_to = request.user
                    file.save()
                    Modification.objects.create(object_type=returned_object_type, object_pk=file.pk,
                                                modified_from_state=file.state, by=request.user)

                except AttributeError as e:
                    messages.error(request, 'Something wrong happened')
            else:
                if file.assigned_to != request.user:


                    messages.error(request, "Permission denied")
        else:
            file = ''
            documents = []
    context = {'results': results, 'file': file, 'documents': list(documents)}
    print(documents)
    return render(request, 'inspect/index.html', context=context)
