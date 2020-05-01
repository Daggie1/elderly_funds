from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from app.models import *

@login_required
def report(request):
    # get all documents
    documents = DocumentFileDetail.objects.all()
    # get all files
    files = DocumentFile.objects.all()
    # get all document types
    document_types = DocumentType.objects.all();
    # get all file types
    file_types = DocumentFileType.objects.all()
    # get all users
    users = User.objects.all()
    reject_file = DocumentFile.objects.filter(
        Q(state='400') | Q(state='401') | Q(state='402') | Q(state='403') | Q(state='404') | Q(state='405') | Q(
            state='406') | Q(state='407') | Q(state='408'))
    reject_document = DocumentFileDetail.objects.filter(
        Q(state='400') | Q(state='401') | Q(state='402') | Q(state='403') | Q(state='404') | Q(state='405') | Q(
            state='406') | Q(state='407') | Q(state='408'))
    registry = DocumentFile.objects.filter(state='300');
    reception = DocumentFile.objects.filter(file_status='301');
    disassembly = DocumentFile.objects.filter(file_status='302')
    qa = DocumentFile.objects.filter(file_status='306');
    scanning = DocumentFile.objects.filter(file_status='303');
    transcription = DocumentFile.objects.filter(file_status='305');
    context = {
        "documents": documents,
        "files": files,
        "document_types": document_types,
        "file_types": file_types,
        "users": users,
        "registry": registry,
        "reception": reception,
        "qa": qa,
        "scanning": scanning,
        "transcription": transcription,
        "disassembly": disassembly,
        "rejected_document": reject_document,
        "rejected_file": reject_file,
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
