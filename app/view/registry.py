from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from app.views import get_file, get_docs
from app.filters import DocumentFileFilter
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib import messages
from app.models import DocumentFile, DocumentFileDetail, Batch, DocumentState
from app.tables import DocumentFileTable
from app.views import get_file, get_docs
from app.models import Modification, Notification
from django.contrib.contenttypes.models import ContentType


def change_file_status(request, pk, object_type, modified_from_state, is_reject_description):
    if is_reject_description != is_reject_description:
        modify_notify_file(request, pk, object_type, modified_from_state, is_reject_description)
    else:
        modify_notify_file(request, pk, object_type, modified_from_state, None)


def change_doc_status(request, pk, object_type, modified_from_state, is_reject_description):
    if is_reject_description != is_reject_description:
        modify_notify_doc(request, pk, object_type, modified_from_state, is_reject_description)
    else:
        modify_notify_doc(request, pk, object_type, modified_from_state, None)


def modify_notify_file(request, pk, modified_from_state, is_reject_description):
    object_key = int(pk)
    returned_object_type = None
    obj = None

    try:
        file = get_file(request, pk)
        if file:
            docs = get_docs([file])
            if docs:

                returned_object_type = ContentType.objects.get(app_label='app', model='documentfiledetail')
                obj = Modification.objects.filter(object_pk=object_key,
                                                  object_type=returned_object_type,
                                                  modified_from_state=modified_from_state).first()
                for doc in docs:


                        Modification.objects.create(object_type=returned_object_type,
                                                    object_pk=object_key,
                                                    modified_from_state_id=modified_from_state,
                                                    modified_to_state=modified_from_state,
                                                    by=obj.by)
                        doc.state_ = modified_from_state
                        doc.save()

            # TODO check if file has doc that is behind or forward

            returned_object_type = ContentType.objects.get(app_label='app', model='documentfile')

            obj = Modification.objects.filter(object_pk=object_key,
                                              object_type=returned_object_type,
                                              modified_from_state=modified_from_state).first()

            initial_modification = Modification.objects.filter(object_type=returned_object_type,
                                                               object_pk=object_key,
                                                               by=request.user,
                                                               modified_from_state=file.state,
                                                               modified_to_state=None,
                                                               modification_ended_at=None).first()
            if initial_modification:
                initial_modification.modification_ended_at = timezone.now()
                initial_modification.modified_to_state = modified_from_state
                initial_modification.save()
                modified_object = Modification.objects.create(object_type=returned_object_type,
                                                              object_pk=object_key,
                                                              modified_from_state_id=modified_from_state,
                                                              by=obj.by)

                if is_reject_description != None:
                    Notification.objects.create(to=obj.by, modification=modified_object, comment=is_reject_description)
                file.state_id = modified_from_state
                file.save()


    except AttributeError as e:
        messages.error(request, ' something wrong happened')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def modify_notify_doc(request, pk,  modified_from_state, is_reject_description):
    object_key = int(pk)
    returned_object_type = None
    obj = None

    try:
        doc = get_one_doc(request, object_key)
        if doc:
            returned_object_type = ContentType.objects.get(app_label='app', model='documentfiledetail')
            obj = Modification.objects.filter(object_pk=object_key,
                                              object_type=returned_object_type,
                                              modified_from_state=modified_from_state).first()

            # TODO document should not be moved past one step of its file,,ie file state_pk=300 doc should only 301 or 401

            initial_modification = Modification.objects.filter(object_type=returned_object_type,
                                                               object_pk=object_key,
                                                               by=request.user,
                                                               modified_from_state=doc.state,
                                                               modified_to_state=None,
                                                               modification_ended_at=None).first()
            if initial_modification:
                initial_modification.modification_ended_at = timezone.now()
                initial_modification.modified_to_state = modified_from_state
                initial_modification.save()
                modified_object = Modification.objects.create(object_type=returned_object_type,
                                                              object_pk=object_key,
                                                              modified_from_state_id=modified_from_state,
                                                              by=obj.by)

                if is_reject_description != None:
                    Notification.objects.create(to=obj.by, modification=modified_object,
                                                comment=is_reject_description)

                doc.state_ = modified_from_state
                doc.save()
    except AttributeError as e:
        messages.error(request, ' something wrong happened')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_one_doc(request, pk=None):
    if not pk == None:

        doc = DocumentFileDetail.objects.get(pk=pk)
        if doc and request.user.has_perm("app." + doc.state.permission.codename):
            return doc

    return None


def get_docs_from_filelist( file_list):
    docs = DocumentFileDetail.objects.filter(file_reference__in=file_list)
    if docs:
        return docs
    return None


def registry_submit_to_receiver(request,batch_id ):
    batch=Batch.objects.get(pk=batch_id)

    if batch:
        files=batch.documentfile_set.all()
        if files:
            docs=get_docs_from_filelist(files)
            if docs:
                docs.update(state_id=301)
                files.update(state_id=301)
                batch.state_id=301
                batch.save()
                messages.success(request, 'Batch submitted successfully')
            else:
                messages.warning(request, 'Empty file!Add some documents then try again')

        else:
            messages.warning(request, 'Empty batch!Add some file then try again')
    else:
        messages.error(request, 'Batch not found')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))