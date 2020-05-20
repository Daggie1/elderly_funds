from app.models import STATES, STAGES,Batch,DocumentFile,DocumentFileDetail
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages

ACTIONS=['Open','Done','Continue_Editing','Close']
def update_state_batch(request, pk, action):
    """update the state of the batch"""
    batch= Batch.objects.get(pk=pk)
    user = request.user
    if batch:
        try:
            if action == ACTIONS[0]:

                batch.open(user=user)
                batch.save()
                messages.success(request, ' Batch status changed successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[1]:
                batch.done()
                batch.save()
                messages.success(request, ' Batch status changed successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[2]:
                batch.continue_editing()
                batch.save()
                messages.success(request, ' Batch status changed successfully')
                return redirect(reverse('files.view', kwargs={'batch_id': batch.id}))
            elif action == ACTIONS[3]:
                batch.close(user=user,comment='')
                batch.save()
                messages.success(request, ' Batch status changed successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, ' No action selected')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        except AttributeError as e:
            messages.error(request, ' something wrong happened while updating batch states')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_state_file(request, pk, action):
    """update the state of the batch"""
    file= DocumentFile.objects.get(pk=pk)
    user = request.user
    if file:
        try:
            if action == ACTIONS[0]:

                file.open(user=user)
                file.save()
                messages.success(request, ' File status changed successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[1]:
                file.done()
                file.save()
                messages.success(request, ' File status changed successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[2]:
                file.continue_editing()
                file.save()
                messages.success(request, ' File status changed successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[3]:
                file.close()
                file.save()
                messages.success(request, ' File status changed successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, ' No action selected')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        except AttributeError as e:
            messages.error(request, ' something wrong happened while updating file status')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def update_state_document(request, pk, action):
    """update the state of the batch"""
    document= DocumentFileDetail.objects.get(pk=pk)
    if document:
        try:
            if action == ACTIONS[0]:

                document.open()
                document.save()
                messages.success(request, ' Document status changed successfully')
                return redirect(reverse('list_document_files'))
            elif action == ACTIONS[1]:
                document.done()
                document.save()
                messages.success(request, ' Document status changed successfully')
                return redirect(reverse('list_document_files'))
            elif action == ACTIONS[3]:
                document.continue_editing()
                document.save()
                messages.success(request, ' Document status changed successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            elif action == ACTIONS[3]:
                document.close()
                document.save()
                messages.success(request, ' Document status changed successfully')
                return redirect(reverse('list_document_files'))
            else:
                messages.error(request, ' No action selected')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except AttributeError as e:
            messages.error(request, ' something wrong happened while updating file status')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
