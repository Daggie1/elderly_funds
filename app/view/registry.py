from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect,reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from app.views import get_file, get_docs_from_file
from app.filters import DocumentFileFilter
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from app.models import DocumentFile, DocumentFileDetail, Batch
from app.tables import DocumentFileTable
from app.views import get_file, get_docs_from_file
from app.models import Modification, Notification
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt




def change_file_status_to_accept(request, pk):
    if request.method == 'POST':
        modified_to_state_id = request.POST.get('modified_to_state_id')
        print(f'modified_to_state_id{modified_to_state_id}')
        if modified_to_state_id != None:
            modified_to_state_id = int(modified_to_state_id) + 1
            return modify_notify_file(request, pk, modified_to_state_id)
        else:
            messages.error('Invalid form')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def change_file_status_to_accept_ajax(request, pk):
    if request.method == 'POST':
        modified_to_state_id = request.POST.get('modified_to_state_id')
        print(f'modified_to_state_id{modified_to_state_id}')
        if modified_to_state_id != None:
            file=DocumentFile.objects.get(pk=pk)
            file.assigned_to=request.user
            file.save()
            modified_to_state_id = int(modified_to_state_id) + 1
            return modify_notify_file(request, pk, modified_to_state_id)
        else:
            messages.error('Invalid form')
    return JsonResponse('done')

def change_file_status_to_reject(request, pk):
    if request.method == 'POST':
        modified_to_state_id = request.POST.get('modified_to_state_id')
        is_reject_description = request.POST.get('is_reject_description')
        if modified_to_state_id != None and is_reject_description != None:
            return modify_notify_file(request, pk, modified_to_state_id, is_reject_description)
        else:
            messages.error('Invalid form')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def return_rectified_file(request, pk):
    if request.method == 'POST':
        modified_to_state_id = request.POST.get('modified_to_state_id')
        if modified_to_state_id != None :
            return modify_notify_file(request, pk, modified_to_state_id, None)
        else:
            messages.error('Invalid form')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def change_document_status_to_accept(request, pk):
    if request.method == 'POST':
        modified_to_state_id = request.POST.get('modified_to_state_id')
        print(f'modified_to_state_id{modified_to_state_id}')
        if modified_to_state_id != None:
            modified_to_state_id = int(modified_to_state_id) + 1
            return modify_notify_doc(request, pk, modified_to_state_id)
        else:
            messages.error('Invalid form')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def change_document_status_to_reject(request, pk):
    if request.method == 'POST':
        modified_to_state_id = request.POST.get('modified_to_state_id')
        is_reject_description = request.POST.get('is_reject_description')
        if modified_to_state_id != None and is_reject_description != None:
            modify_notify_doc(request, pk, modified_to_state_id, is_reject_description)
        else:
            messages.error('Invalid form')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def modify_notify_file(request, pk, modified_to_state_id, is_reject_description=None):
    object_key = pk

    returned_object_type = None
    file_obj = None

    try:

        file = get_file(request, object_key)
        if file:

            returned_object_type = ContentType.objects.get(app_label='app', model='documentfile')
            file_obj = Modification.objects.filter(object_pk=object_key,
                                                   object_type=returned_object_type,
                                                   modified_from_state=file.state,
                                                   modified_to_state=None,
                                                   by=request.user).last()
            if file_obj==None:
                Modification.objects.create(object_pk=object_key,
                                                   object_type=returned_object_type,
                                                   modified_from_state=file.state,

                                                   by=request.user)
                file_obj = Modification.objects.filter(object_pk=object_key,
                                                       object_type=returned_object_type,
                                                       modified_from_state=file.state,
                                                       modified_to_state=None,
                                                       by=request.user).last()

            if file.assigned_to == request.user:

                print('is assigned')
                docs = get_docs_from_file(request, file)

                if docs:

                    returned_object_type = ContentType.objects.get(app_label='app', model='documentfiledetail')

                    for doc in docs:
                        Modification.objects.create(object_type=returned_object_type,
                                                    object_pk=object_key,
                                                    modified_from_state_id=file_obj.modified_from_state_id,
                                                    modified_to_state_id=modified_to_state_id,
                                                    modification_started_at=file_obj.modification_started_at,
                                                    modification_ended_at=timezone.now(),
                                                    by=file_obj.by)
                        doc.assigned_to=None
                        doc.state_id= modified_to_state_id
                        doc.save()

                file_obj.modified_to_state_id = modified_to_state_id
                file_obj.modification_ended_at = timezone.now()

                file.assigned_to=None
                file_obj.save()

                file.state_id = modified_to_state_id
                file.save()

                if is_reject_description != None:
                    returned_object_type = ContentType.objects.get(app_label='app', model='documentfile')

                    who_edited_the_escalated_state = Modification.objects.filter(object_pk=object_key,
                                                                                 object_type=returned_object_type,
                                                                                 modified_from_state_id=int(
                                                                                     modified_to_state_id) - 100
                                                                                 ).exclude(modified_to_state=None).last()
                    Modification.objects.create(object_type=returned_object_type, object_pk=file.pk,
                                                                 modified_from_state_id=modified_to_state_id,
                                                                 by=who_edited_the_escalated_state.by)
                    Notification.objects.create(to=who_edited_the_escalated_state.by, modification=file_obj,
                                                    comment=is_reject_description)
                    admins = User.objects.filter(is_superuser=True)
                    for admin in admins:
                        Notification.objects.create(to=admin, modification=file_obj,
                                                    comment=is_reject_description)
                    file.assigned_to =who_edited_the_escalated_state.by

                    file.save()
                return redirect(reverse('list_document_files'))
            else:
                messages.error(request,"You don't have the permissions to edit this file")
        else:
            messages.error(request, "You don't have the permission to edit this file")

    except AttributeError as e:
        messages.error(request, ' something wrong happened')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def modify_notify_doc(request, pk, modified_to_state_id, is_reject_description=None):
    object_key = pk

    returned_object_type = None
    doc_obj = None

    try:

        doc = get_one_doc(request, int(object_key))
        if doc:

            returned_object_type = ContentType.objects.get(app_label='app', model='documentfiledetail')
            doc_obj = Modification.objects.filter(object_pk=object_key,
                                                   object_type=returned_object_type,
                                                   modified_from_state=doc.state,
                                                   modified_to_state=None,
                                                   by=request.user).last()
            if doc.file_reference.assigned_to == request.user:

                doc_obj = Modification.objects.filter(object_pk=object_key,
                                                      object_type=returned_object_type,
                                                      modified_from_state=doc.state,
                                                      modified_to_state=None,
                                                      by=request.user).last()
                if not doc_obj:
                    doc_obj=Modification.objects.create(object_pk=object_key,
                                                      object_type=returned_object_type,
                                                      modified_from_state=doc.state,

                                                      by=request.user)

                doc_obj.modified_to_state_id = modified_to_state_id
                doc_obj.modification_ended_at = timezone.now()
                doc_obj.save()


                if is_reject_description != None:
                    returned_object_type = ContentType.objects.get(app_label='app', model='documentfiledetail')

                    who_edited_the_escalated_state = Modification.objects.filter(object_pk=object_key,
                                                                                 object_type=returned_object_type,
                                                                                 modified_from_state_id=int(
                                                                                     modified_to_state_id) - 100
                                                                                 ).exclude(
                        modified_to_state=None).last()
                    Modification.objects.create(object_type=returned_object_type, object_pk=doc.pk,
                                                modified_from_state_id=modified_to_state_id,
                                                by=who_edited_the_escalated_state.by)
                    Notification.objects.create(to=who_edited_the_escalated_state.by, modification=doc_obj,
                                                comment=is_reject_description)

                    admins=User.objects.filter(is_superuser=True)
                    for admin in admins:
                        Notification.objects.create(to=admin, modification=doc_obj,
                                                    comment=is_reject_description)
                return redirect(reverse('list_document_files'))
            else:
                messages.error(request, "You don't have the permission to edit this document")
        else:
            messages.error(request, "You don't have the permission to edit this document")

    except AttributeError as e:
        messages.error(request, ' something wrong happened')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_one_doc(request, pk=None):
    if not pk == None:

        doc = DocumentFileDetail.objects.get(pk=pk)
        if doc and request.user.has_perm("app." + doc.state.permission.codename):
            return doc

    return None


def get_docs_from_filelist(file_list):
    docs = DocumentFileDetail.objects.filter(file_reference__in=file_list)
    if docs:
        return docs
    return None


def registry_submit_to_receiver(request, batch_id):
    batch = Batch.objects.get(pk=batch_id)

    if batch:
        files = batch.documentfile_set.all()
        if files:
            docs = get_docs_from_filelist(files)
            if docs:
                returned_object_type = ContentType.objects.get(app_label='app', model='documentfiledetail')
                for doc in docs:

                    Modification.objects.create(object_type=returned_object_type,
                                                object_pk=doc.pk,
                                                modified_from_state_id=batch.state_id,
                                                modified_to_state_id=301,
                                                modification_started_at=batch.created_on,
                                                modification_ended_at=timezone.now(),
                                                by=batch.created_by)
                docs.update(state_id=301)
                returned_object_type = ContentType.objects.get(app_label='app', model='documentfile')
                for file in files:
                    Modification.objects.create(object_type=returned_object_type,
                                                object_pk=file.pk,
                                                modified_from_state_id=batch.state_id,
                                                modified_to_state_id=301,
                                                modification_started_at=batch.created_on,
                                                modification_ended_at=timezone.now(),
                                                by=batch.created_by)
                files.update(state_id=301)
                batch.state_id = 301
                batch.save()
                messages.success(request, 'Batch submitted successfully')
            else:
                messages.warning(request, 'Empty file!Add some documents then try again')

        else:
            messages.warning(request, 'Empty batch!Add some file then try again')
    else:
        messages.error(request, 'Batch not found')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
