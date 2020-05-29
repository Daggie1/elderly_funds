from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse_lazy

from django.utils import timezone
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, RequestConfig
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from app.filters import DocumentFileFilter
from app.models import DocumentFile, STAGES, STATES
from app.tables import DocumentFileTable, EscalatedFileTable


class RejectedDocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'
    filterset_class = DocumentFileFilter
    table_class = EscalatedFileTable
    template_name = 'view_document_files.html'

    def get_queryset(self):
        #mark all as read
        self.request.user.notificationsentto_set.filter(read_at__isnull=True).update(read_at=timezone.now())

        if self.request.user.is_superuser:
            queryset = DocumentFile.objects.filter(flagged=True)
        elif self.request.user.has_perm('app.can_create_batch'):
            queryset = DocumentFile.objects.filter(stage=STAGES[0], flagged=True).filter(
                Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_receive_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[1], flagged=True).filter(
                Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_disassemble_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[2], flagged=True).filter(
                Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_scan_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[3], flagged=True).filter(
                Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_transcribe_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[4], flagged=True).filter(
                Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_qa_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[5], flagged=True).filter(
                Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_validate_file'):
            queryset = DocumentFile.objects.filter(stage=STAGES[6], flagged=True).filter(
                Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        else:
            queryset = DocumentFile.objects.none()

        self.table = EscalatedFileTable(queryset)
        self.filter = DocumentFileFilter(self.request.GET,
                                         queryset)
        self.table = EscalatedFileTable(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['table'] = self.table
        context['filter'] = self.filter
        return context
