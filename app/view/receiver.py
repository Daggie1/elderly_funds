
from django.shortcuts import redirect, reverse

from django.http import HttpResponseRedirect
from django.contrib import messages

from app.views import get_file, get_docs_from_file
from app.models import Modification, Notification
from django.contrib.contenttypes.models import ContentType


def select_file(request, pk):
    file = get_file(request, pk)
    if file:


        if  file.assigned_to == None:
            returned_object_type = ContentType.objects.get(app_label='app', model='documentfile')
            print(f'returned_obj={returned_object_type}')
            try:
                file.assigned_to=request.user
                file.save()
                Modification.objects.create(object_type=returned_object_type, object_pk=file.pk,
                                            modified_from_state=file.state, by=request.user)
                if request.user.has_perm("app.can_scan_file"):
                    return redirect(reverse('upload_document', kwargs={'file_reference': file.pk}))
                else:
                    return redirect(reverse('view_docs_in_file', kwargs={'file_reference': file.pk}))
            except AttributeError as e:
                messages.error(request, 'Something wrong happened')
        else:
            if file.assigned_to == request.user:
                if request.user.has_perm("app.can_scan_file"):
                    return redirect(reverse('upload_document', kwargs={'file_reference': file.pk}))
                else:
                    return redirect(reverse('view_docs_in_file', kwargs={'file_reference': file.pk}))
            else:
                messages.error(request, "Permission denied")
    else:
        messages.error(request, "Permission denied")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
