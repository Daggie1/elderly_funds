from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from app.filters import DocumentFileFilter
from app.models import DocumentFile, Batch,DocumentState
from app.tables import DocumentFileTable


class DocumentFileCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documentfile'
    success_message = 'Added created successfully'
    model = DocumentFile
    template_name = 'file/create.html'
    fields = ['file_reference', 'file_type', 'file_barcode']





    def form_valid(self, form):
        form.instance.file_created_by = self.request.user
        form.instance.state_id = 300
        form.instance.batch_id = self.kwargs['batch_id']
        # file=form.save()
        # print(file.file_reference)
        return super().form_valid(form)
            # reverse_lazy('document.view', kwargrs={'file_ref_no': file.file_reference})


class FilesView(LoginRequiredMixin,  SingleTableMixin, FilterView):
    template_name = 'file/index.html'
    table_class = DocumentFileTable
    def get_context_data(self,  **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['batch_id']=int(self.kwargs['batch_id'])
        print(context)
        return context

    def get_queryset(self):
        return DocumentFile.objects.filter(batch_id=int(self.kwargs['batch_id']))

    filterset_class = DocumentFileFilter
    # def get(self, request, *args, **kwargs):
    #     batch_id = kwargs['batch_id']
    #     files = DocumentFile.objects.filter(batch=Batch.objects.get(pk=batch_id))
    #
    #
    #     return render(request, 'file/index.html', {
    #         'object_list': files,
    #         'batch_id': batch_id
    #     })


class DocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'

    table_class = DocumentFileTable
    template_name = 'view_document_files.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DocumentFile.objects.all()
        elif self.request.user.has_perm('app.can_scan_file'):
            filter = DocumentFile.objects.filter(state_id=302)
            list_isNull = filter.filter(file_scanned_by__isnull=True)
            list_filled = filter.filter(file_scanned_by=self.request.user)
            return list_isNull.union(list_filled)

        elif self.request.user.has_perm('app.can_transcribe_file'):
            return DocumentFile.objects.filter(state_id=303 ).filter(file_transcribed_by=self.request.user)

        elif self.request.user.has_perm('app.can_qa_file'):
            filter=DocumentFile.objects.filter(state_id=304)
            list_isNull=filter.filter( file_qa_by__isnull=True )
            list_filled=filter.filter(file_qa_by=self.request.user)
            return list_isNull.union(list_filled)

        elif self.request.user.has_perm('app.can_validate_file'):
            filter = DocumentFile.objects.filter(state_id=305)
            list_isNull = filter.filter(file_validated_by__isnull=True)
            list_filled = filter.filter(file_validated_by=self.request.user)
            return list_isNull.union(list_filled)

    filterset_class = DocumentFileFilter
