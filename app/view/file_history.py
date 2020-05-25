from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User,Permission
from app.models import DocumentFile, Modification,STAGES
from django.shortcuts import render
from app.tables import HistoryTable,SpecificFileUserHistoryTable
from django.db.models import Count


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

    if user.is_superuser:
        # table = HistoryTable(Modification.objects.filter(by=user))
        table = HistoryTable(Modification.objects.distinct('file'))

    else:
        table = HistoryTable(Modification.objects.filter(by=user).distinct('file'))
    return render(request, 'user/history.html', {'table': table})

def user_specific_file_history(request,pk):
    user = request.user
    file=DocumentFile.objects.get(pk=pk)
    if user and file:
        table = SpecificFileUserHistoryTable(Modification.objects.filter(by=user,file=file))
        return render(request, 'user/specific_user_file_history.html', {'table': table,
                                                     'file':file.__str__()})

def file_details(request,pk):
    file=DocumentFile.objects.get(pk=pk)
    data={}
    if file:
        data.update({'file': file})
        stage=file.stage
        pk=56
        kl=list()

        stage_index=STAGES.index(file.stage)
        print(stage_index)
        users=User.objects.filter(groups__permissions=65 + int(stage_index))
        data.update({'users': users})

    return  render(request,'file/details.html',data)
def assign_file(request,pk):
    if request.method == 'POST':
        user=User.objects.get(pk=request.POST.get('assigned_user'))
        print (f'user={user}')
        file=DocumentFile.objects.get(pk=pk)
        if user :
            if file:
                file.assigned_to=user
                file.save()
                messages.warning(request, 'Assigned successfully ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))