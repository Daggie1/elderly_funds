from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from app.models import *


@login_required
def report(request):
    MAX = 5
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

    registry = DocumentFile.objects.filter(stage=STAGES[0]).order_by('-created_on')
    reception = DocumentFile.objects.filter(stage=STAGES[1]).order_by('-created_on')
    disassembly = DocumentFile.objects.filter(stage=STAGES[2]).order_by('-created_on')
    transcription = DocumentFile.objects.filter(stage=STAGES[3]).order_by('-created_on')
    qa = DocumentFile.objects.filter(stage=STAGES[4]).order_by('-created_on')
    scanning = DocumentFile.objects.filter(stage=STAGES[5]).order_by('-created_on')

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



def send_report_message(request):
    report = request.GET.get('reasons')
    Notification.objects.create(comment=report, created_by=request.user)
    # notification.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_messages(request):
    messages = Notification.objects.filter(file_id=None).filter(resolved=False).order_by('-created_at')[:20]
    return render(request, 'messages.html', {'messages': messages})


def mark_as_resolved(request, id):
    message = Notification.objects.get(pk=id)
    message.resolved_by = request.user
    message.resolved = True
    message.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_document_type(request, id):
    document_type = DocumentType.objects.filter(pk=id)
    document_type.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
