from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from app.filters import DocumentFileFilter
from app.models import DocumentFile, DocumentFileDetail
from app.tables import QaTable,ValidateQADocTable


class QaFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'

    table_class = QaTable
    template_name = 'qa/index.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DocumentFile.objects.all()
        elif self.request.user.has_perm('app.can_receive_file'):

            q1 = DocumentFile.objects.filter(state_id = 301,
                                               assigned_to = self.request.user)
            q2 = DocumentFile.objects.filter(state_id = 301,
                                               assigned_to = None)
            return q1.union(q2)
        elif self.request.user.has_perm('app.can_disassemble_file'):

            q1 = DocumentFile.objects.filter(state_id=302,
                                             assigned_to=self.request.user)
            q2 = DocumentFile.objects.filter(state_id=302,
                                             assigned_to=None)
            return q1.union(q2)
        elif self.request.user.has_perm('app.can_scan_file'):

            q1 = DocumentFile.objects.filter(state_id=303,
                                             assigned_to=self.request.user)
            q2 = DocumentFile.objects.filter(state_id=303,
                                             assigned_to=None)
            return q1.union(q2)
        elif self.request.user.has_perm('app.can_reassemble_file'):

            q1 = DocumentFile.objects.filter(state_id=304,
                                             assigned_to=self.request.user)
            q2 = DocumentFile.objects.filter(state_id=304,
                                             assigned_to=None)
            return q1.union(q2)

        elif self.request.user.has_perm('app.can_transcribe_file'):
            q1 = DocumentFile.objects.filter(state_id=305,
                                             assigned_to=self.request.user)
            q2 = DocumentFile.objects.filter(state_id=305,
                                             assigned_to=None)
            return q1.union(q2)

        elif self.request.user.has_perm('app.can_qa_file'):
            q1 = DocumentFile.objects.filter(state_id=306,
                                             assigned_to=self.request.user)
            q2 = DocumentFile.objects.filter(state_id=306,
                                             assigned_to=None)
            return q1.union(q2)

        elif self.request.user.has_perm('app.can_validate_file'):
            q1 = DocumentFile.objects.filter(state_id=307,
                                             assigned_to=self.request.user)
            q2 = DocumentFile.objects.filter(state_id=307,
                                             assigned_to=None)
            return q1.union(q2)

    filterset_class = DocumentFileFilter


def open_file_for_qa(request,id):
    file = DocumentFile.objects.get(pk=id)
    table= ValidateQADocTable(DocumentFileDetail.objects.filter(file_reference=id))
    return render(request, 'qa/documents.html', {'file':file,'table':table})