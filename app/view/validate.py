from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from app.filters import DocumentFileFilter
from app.models import DocumentFile, DocumentFileDetail
from app.tables import ValidationTable, ValidateQADocTable
from app.models import STAGES

class ValidateFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'
    filterset_class = DocumentFileFilter

    table_class = ValidationTable
    template_name = 'validate/index.html'

    def get_queryset(self):
        return DocumentFile.objects.filter(stage=STAGES[6])


def open_file_for_Validator(request, id):
    file = DocumentFile.objects.get(pk=id)
    table = ValidateQADocTable(DocumentFileDetail.objects.filter(file_reference=id))
    return render(request, 'qa/documents.html', {'file': file, 'table': table})
