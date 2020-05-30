from json2html import *
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect, render
from django.db.models import Q
from django.urls import reverse_lazy, reverse

from django.utils import timezone
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, RequestConfig
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView, UpdateView
from app.filters import DocumentFileFilter
from app.models import DocumentFile, STAGES, STATES, DocumentFileDetail
from app.tables import DocumentFileTable, BatchFileTable, CompleteFiles


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
        return reverse('batch_files', kwargs={'pk': self.kwargs['batch_id']})


class FilesView(LoginRequiredMixin, SingleTableMixin, FilterView):
    template_name = 'file/index.html'
    table_class = DocumentFileTable

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books

        context['batch_id'] = int(self.kwargs['batch_id'])

        return context

    def get_queryset(self):
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)
        if self.request.user.has_perm('app.can_register_batch'):
            return DocumentFile.objects.filter(batch_id=int(self.kwargs['batch_id']))
        elif self.request.user.has_perm('app.can_receive_file'):

            q1 = DocumentFile.objects.filter(state_id=301,
                                             batch_id=int(self.kwargs['batch_id']),
                                             assigned_to=self.request.user)
            q2 = DocumentFile.objects.filter(state_id=301,
                                             batch_id=int(self.kwargs['batch_id']),
                                             assigned_to=None)
            return q1.union(q2)

    filterset_class = DocumentFileFilter


# TODO check states (Tuple Out Of Index)
class DocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'

    table_class = DocumentFileTable
    template_name = 'view_document_files.html'
    filterset_class = DocumentFileFilter

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = DocumentFile.objects.all()
        elif self.request.user.has_perm('app.can_create_batch'):
            queryset = DocumentFile.objects.filter(stage=STAGES[0], flagged=False).filter(
                Q(assigned_to=self.request.user) | Q(assigned_to__isnull=True) )
        elif self.request.user.has_perm('app.can_receive_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[1], flagged=False).filter(
                Q(assigned_to=self.request.user))
        elif self.request.user.has_perm('app.can_disassemble_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[2], flagged=False).filter(
                Q(assigned_to=self.request.user) )
        elif self.request.user.has_perm('app.can_scan_file'):

            queryset = DocumentFile.objects.filter(stage=STAGES[3], flagged=False).filter(
                Q(assigned_to=self.request.user) | Q(assigned_to__isnull=True))



        elif self.request.user.has_perm('app.can_transcribe_file'):

            queryset = DocumentFile.objects.filter(stage=STAGES[4], flagged=False).filter(
                Q(assigned_to=self.request.user) | Q(assigned_to__isnull=True) )


        elif self.request.user.has_perm('app.can_qa_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[5], flagged=False).filter(
                Q(assigned_to=self.request.user) | Q(assigned_to__isnull=True) )

        elif self.request.user.has_perm('app.can_validate_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[6], flagged=False).filter(
                Q(assigned_to=self.request.user) | Q(assigned_to__isnull=True) )
        else:
            queryset = DocumentFile.objects.none()

        self.table = DocumentFileTable(queryset)
        self.filter = DocumentFileFilter(self.request.GET,
                                         queryset)
        self.table = DocumentFileTable(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['table'] = self.table
        context['filter'] = self.filter
        return context


class RejectedDocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = DocumentFileTable
    template_name = 'file/rejected_file_documents_list.html'

    def get_queryset(self):
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)
        if self.request.user.is_superuser:
            return DocumentFile.objects.DocumentFile.objects.filter(
                flagged=True)
        elif self.request.user.has_perm('app.can_create_batch'):
            return DocumentFile.objects.filter(flagged=True).filter(
                stage=STAGES[0],
                assigned_to=self.request.user)
        elif self.request.user.has_perm('app.can_receive_file'):
            return DocumentFile.objects.filter(flagged=True).filter(
                stage=STAGES[1],
                assigned_to=self.request.user)
        elif self.request.user.has_perm('app.can_disassemble_file'):
            return DocumentFile.objects.filter(flagged=True).filter(
                stage=STAGES[2],
                assigned_to=self.request.user)
        elif self.request.user.has_perm('app.can_scan_file'):

            return DocumentFile.objects.filter(flagged=True).filter(
                stage=STAGES[3],
                assigned_to=self.request.user)


        elif self.request.user.has_perm('app.can_transcribe_file'):

            return DocumentFile.objects.filter(flagged=True).filter(
                stage=STAGES[4],
                assigned_to=self.request.user)

        elif self.request.user.has_perm('app.can_qa_file'):
            return DocumentFile.objects.filter(flagged=True).filter(
                stage=STAGES[5],
                assigned_to=self.request.user)

        elif self.request.user.has_perm('app.can_validate_file'):
            return DocumentFile.objects.filter(flagged=True).filter(
                stage=STAGES[6],
                assigned_to=self.request.user)
        else:
            return DocumentFile.objects.none()

    filterset_class = DocumentFileFilter


class FileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = DocumentFile
    fields = ['file_type', 'file_reference', 'file_barcode']
    template_name = 'file/create.html'
    success_message = 'File updated successfully'

    def form_valid(self, form):
        form.instance.file_created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        file = self.get_object()
        if self.request.user.has_perm('app.can_register_batch'):
            return True
        return False


class FileDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = DocumentFile
    success_url = reverse_lazy('list_document_files')
    success_message = 'File Deleted Successfully'
    template_name = 'file/delete_confirm.html'

    def test_func(self):
        if self.request.user.has_perm('app.can_register_batch'):
            return True
        return False


# open a complete file
# see all its contents


class CompleteFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'
    table_class = CompleteFiles
    template_name = 'view_document_files.html'
    filterset_class = DocumentFileFilter

    def get_queryset(self):
        queryset = DocumentFile.objects.filter( Q(stage=STAGES[7]))
        self.table = CompleteFiles(queryset)
        self.filter = DocumentFileFilter(self.request.GET,
                                         queryset)
        self.table = CompleteFiles(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['table'] = self.table
        context['filter'] = self.filter
        return context


def file_internals(request, id):
    documents = DocumentFileDetail.objects.filter(file_reference=id)
    large_table = []
    for document in documents:
        content = document.document_content
        table_data = json2html.convert(json=content, table_attributes="id=\"info-table\" class=\"table table-bordered "
                                                                  "table-hover\"")
        large_table.append(table_data)

    return render(request, 'file/pages.html', {'table_data': large_table})
