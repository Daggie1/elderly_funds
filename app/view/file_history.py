from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from app.serializers import DocumentSerializer
from django.contrib.auth.models import User
from app.models import DocumentFile, Modification

def get_file_history(request, pk):
    file=DocumentFile.objects.get(pk=pk)
    if file:
        all_modification=file.modification_set.all()
        return all_modification
    else:
        return Modification.objects.none()#

def get_each_user_history(request, pk):
    user=User.objects.get(pk=pk)
    if user:
       return user.modification_set.all()
    else:
        return Modification.objects.none()

def get_loggedin_user_history(request):
    user=request.user
    if user:
       return user.modification_set.all()
    else:
        return Modification.objects.none()
