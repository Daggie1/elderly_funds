from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse_lazy, reverse

from django.utils import timezone
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from app.filters import DocumentFileFilter
from app.models import DocumentFile, STAGES, STATES
from app.tables import DocumentFileTable, BatchFileTable


class DocumentFileCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documentfile'
    success_message = 'File created successfully'
    model = DocumentFile
    template_name = 'file/create.html'
    fields = ['file_reference', 'file_type', 'file_barcode']

    def form_valid(self, form):
        form.instance.file_created_by = self.request.user

        form.instance.batch_id = self.kwargs['batch_id']
        # file=form.save()
        # print(file.file_reference)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('batch_files', kwargs={'batch_id': self.kwargs['batch_id']})

class FilesView(LoginRequiredMixin, SingleTableMixin, FilterView):
    template_name = 'file/index.html'
    table_class = DocumentFileTable

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books

        context['batch_id']=int(self.kwargs['batch_id'])


        return context

    def get_queryset(self):

        return DocumentFile.objects.filter(batch_id=int(self.kwargs['batch_id']))


    filterset_class = DocumentFileFilter


# TODO check states (Tuple Out Of Index)
class DocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'

    table_class = DocumentFileTable
    template_name = 'view_document_files.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DocumentFile.objects.all()
        elif self.request.user.has_perm('app.can_create_batch'):
            return DocumentFile.objects.filter(stage=STAGES[0],flagged=False).filter(Q(assigned_to=self.request.user) |Q(assigned_to__isnull=True) | Q(state=STATES[2]))
        elif self.request.user.has_perm('app.can_receive_file'):
            return DocumentFile.objects.filter(stage=STAGES[1],flagged=False).filter(Q(assigned_to=self.request.user) |Q(assigned_to__isnull=True) | Q(state=STATES[2]))
        elif self.request.user.has_perm('app.can_disassemble_file'):
            return DocumentFile.objects.filter(stage=STAGES[2],flagged=False).filter(Q(assigned_to=self.request.user) |Q(assigned_to__isnull=True) | Q(state=STATES[2]))
        elif self.request.user.has_perm('app.can_scan_file'):

         return DocumentFile.objects.filter(stage=STAGES[3],flagged=False).filter(Q(assigned_to=self.request.user) |Q(assigned_to__isnull=True) | Q(state=STATES[2]))



        elif self.request.user.has_perm('app.can_transcribe_file'):



            return DocumentFile.objects.filter(stage=STAGES[4],flagged=False).filter(Q(assigned_to=self.request.user) |Q(assigned_to__isnull=True) | Q(state=STATES[2]))


        elif self.request.user.has_perm('app.can_qa_file'):
            return DocumentFile.objects.filter(stage=STAGES[5],flagged=False).filter(Q(assigned_to=self.request.user) |Q(assigned_to__isnull=True) | Q(state=STATES[2]))

        elif self.request.user.has_perm('app.can_validate_file'):
            return DocumentFile.objects.filter(stage=STAGES[6],flagged=False).filter(Q(assigned_to=self.request.user) |Q(assigned_to__isnull=True) | Q(state=STATES[2]))
        else:
            return DocumentFile.objects.none()

    filterset_class = DocumentFileFilter


class RejectedDocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = DocumentFileTable
    template_name = 'file/rejected_file_documents_list.html'

    def get_queryset(self):

        if self.request.user.is_superuser:
            return DocumentFile.objects.DocumentFile.objects.filter(
                flagged=True)
        elif self.request.user.has_perm('app.can_create_batch'):
            return DocumentFile.objects.filter(stage=STAGES[0]).filter(
                flagged=True,
                assigned_to=self.request.user)
        elif self.request.user.has_perm('app.can_receive_file'):
            return DocumentFile.objects.filter(stage=STAGES[1]).filter(
                flagged=True,
                assigned_to=self.request.user)
        elif self.request.user.has_perm('app.can_disassemble_file'):
            return DocumentFile.objects.filter(stage=STAGES[2]).filter(
                flagged=True,
                assigned_to=self.request.user)
        elif self.request.user.has_perm('app.can_scan_file'):

            return DocumentFile.objects.filter(stage=STAGES[3]).filter(
                flagged=True,
                assigned_to=self.request.user)


        elif self.request.user.has_perm('app.can_transcribe_file'):

            return DocumentFile.objects.filter(stage=STAGES[4]).filter(
                flagged=True,
                assigned_to=self.request.user)

        elif self.request.user.has_perm('app.can_qa_file'):
            return DocumentFile.objects.filter(stage=STAGES[5]).filter(
                flagged=True,
                assigned_to=self.request.user)

        elif self.request.user.has_perm('app.can_validate_file'):
            return DocumentFile.objects.filter(stage=STAGES[6]).filter(
                flagged=True,
                assigned_to=self.request.user)
        else:
            return DocumentFile.objects.none()

    filterset_class = DocumentFileFilter


class FileDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = DocumentFile
    success_url = reverse_lazy('list_document_files')
    success_message = 'File Deleted Successfully'
    template_name = 'file/delete_confirm.html'

    def test_func(self):
        batch = self.get_object()
        if self.request.user.has_perm('app.can_register_batch'):
            return True
        return False
