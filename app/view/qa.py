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
        return DocumentFile.objects.filter(stage=[5]).filter(
            flagged=True,
            assigned_to=self.request.user)

    filterset_class = DocumentFileFilter


def open_file_for_qa(request,id):
    file = DocumentFile.objects.get(pk=id)
    table= ValidateQADocTable(DocumentFileDetail.objects.filter(file_reference=id))
    return render(request, 'qa/documents.html', {'file':file,'table':table})