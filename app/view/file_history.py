from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from app.serializers import DocumentSerializer
from django.contrib.auth.models import User
from app.models import DocumentFile, Modification
from django.shortcuts import render
from app.tables import HistoryTable


def get_file_history(request, pk):
    file = DocumentFile.objects.get(pk=pk)
    if file:
        history = file.modification_set.all()
    else:
        history = Modification.objects.none()
    return render(request, 'file/file_history.html', {'file': file, 'history': history})


def get_each_user_history(request, pk):
    user = User.objects.get(pk=pk)
    if user:
        return user.modification_set.all()
    else:
        return Modification.objects.none()


def get_loggedin_user_history(request):
    user = request.user

    if user:
        table = HistoryTable(user.modification_set.all())
    else:
        table = HistoryTable(Modification.objects.none())
    return render(request, 'user/history.html', {'table': table})
