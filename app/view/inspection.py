from django.shortcuts import render

from app.models import DocumentFileDetail, DocumentFile


def inspect(request):
    # make a query
    return render(request, 'inspect/index.html')
