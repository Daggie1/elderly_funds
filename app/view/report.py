from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from app.models import *


@login_required
def report(request):


    return render(request, "home.html")



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
