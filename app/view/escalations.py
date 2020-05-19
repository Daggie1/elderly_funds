from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse_lazy

from django.utils import timezone
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from app.filters import DocumentFileFilter
from app.models import DocumentFile, STAGES,STATES
from app.tables import DocumentFileTable






class DocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'

    table_class = DocumentFileTable
    template_name = 'view_document_files.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DocumentFile.objects.all()
        elif self.request.user.has_perm('app.can_create_batch'):
            return DocumentFile.objects.filter(stage=STAGES[0],flagged=True).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_receive_file'):
            return DocumentFile.objects.filter(stage=STAGES[1],flagged=True).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_disassemble_file'):
            return DocumentFile.objects.filter(stage=STAGES[2],flagged=True).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_scan_file'):

         return DocumentFile.objects.filter(stage=STAGES[3],flagged=True).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))


        elif self.request.user.has_perm('app.can_transcribe_file'):


            return DocumentFile.objects.filter(stage=STAGES[4],flagged=True).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))

        elif self.request.user.has_perm('app.can_qa_file'):
            return DocumentFile.objects.filter(stage=STAGES[5],flagged=True).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))

        elif self.request.user.has_perm('app.can_validate_file'):
            return DocumentFile.objects.filter(stage=STAGES[6],flagged=True).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        else:
            return DocumentFile.objects.none()
    filterset_class = DocumentFileFilter
