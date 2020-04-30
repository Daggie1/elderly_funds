from django.db.models import Q
from django.shortcuts import render

from app.models import DocumentFileDetail, DocumentFile


def inspect(request,id=None):
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
            documents = DocumentFileDetail.objects.filter(file_reference=id).values()
            file = DocumentFile.objects.get(pk=id)
        else:
            file = ''
            documents = []
    context = {'results': results, 'file':file,'documents':documents}
    print(results)
    return render(request, 'inspect/index.html',context=context)


def receive(request, id):
    # files = DocumentFile.objects.get(pk=id)
    return render(request, 'inspect/receiver.html')
