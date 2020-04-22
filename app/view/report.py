from django.shortcuts import render
from django.contrib.auth.models import User

from app.models import *


def report(request):
    # get all documents
    documents = DocumentFileDetail.objects.all()
    # get all files
    files = DocumentFile.objects.all()
    # get all document types
    document_types = DocumentType.objects.all();
    # get all file types
    file_types = DocumentFileType.objects.all()
    #get all users
    users = User.objects.all()
    registry = DocumentFile.objects.filter(file_status = 'registry');
    reception = DocumentFile.objects.filter(file_status = 'reception');
    disassembly = DocumentFile.objects.filter(file_status = 'disassembly');
    scanning = DocumentFile.objects.filter(file_status = 'scanning');
    transcription = DocumentFile.objects.filter(file_status = 'transcription');
    context = {
        "documents": documents,
        "files": files,
        "document_types": document_types,
        "file_types": file_types,
        "users":users
    }

    return render(request, "home.html", context)


def get_rejected_documents():
    pass


def get_accepted_documents():
    pass


def track_files():
    pass


def get_escalated_issues():
    pass


def open_file():
    pass
