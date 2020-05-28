from django.http import HttpResponseRedirect
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
    document_types = DocumentType.objects.all()
    # get all file types
    file_types = DocumentFileType.objects.all()
    # get all users
    users = User.objects.all()

    file = DocumentFile.objects.first()

    reject_file = DocumentFile.objects.filter(
        flagged=True)

    registry = DocumentFile.objects.filter(stage=STAGES[0])
    reception = DocumentFile.objects.filter(stage=STAGES[1])
    disassembly = DocumentFile.objects.filter(stage=STAGES[2])
    transcription = DocumentFile.objects.filter(stage=STAGES[3])
    qa = DocumentFile.objects.filter(stage=STAGES[4])
    scanning = DocumentFile.objects.filter(stage=STAGES[5])

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


def send_report_message(request):
    report = request.GET.get('reasons')
    Notification.objects.create(comment=report, created_by=request.user)
    # notification.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
