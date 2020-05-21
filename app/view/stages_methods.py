from app.models import DocumentFile
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

ACTIONS=['Dispatch to Reception',
         'Return to Registry', 'Dispatch to Assembler',
         'Return to Reception', 'Dispatch to Scanner',
         'Dispatch to Transcriber',
         'Dispatch to QA',
         'Dispatch to Validator',
         'Finalize to Reception']


def update_stage_file(request, pk, action):
    rejection_comment=''
    """update the stages of the batch"""
    file= DocumentFile.objects.get(pk=pk)
    user = request.user
    if file:
        try:
            if action == ACTIONS[0]:
                file.dispatch_reception(user=user)
                file.save()
                messages.success(request, ' File moved successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[1]:
                file.return_registry(user=user,rejection_comment=rejection_comment)
                file.save()
                messages.success(request, ' File moved successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[2]:
                file.dispatch_assembly(user=user)
                file.save()
                messages.success(request, ' File moved successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[3]:
                file.return_reception(user=user,rejection_comment=rejection_comment)
                file.save()
                messages.success(request, ' File moved successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[4]:
                file.dispatch_scanner(user=user)
                file.save()
                messages.success(request, ' File moved successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[5]:
                file.dispatch_transcriber(user=user)
                file.save()
                messages.success(request, ' File moved successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[6]:
                file.dispatch_qa(user=user)
                file.save()
                messages.success(request, ' File moved successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[7]:
                file.dispatch_validator(user=user)
                file.save()
                messages.success(request, ' File moved successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif action == ACTIONS[8]:
                file.finalize_to_reception()
                file.save()
                messages.success(request, ' File moved successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, ' No action selected')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except AttributeError as e:
            messages.error(request, ' something wrong happened while updating file status')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))