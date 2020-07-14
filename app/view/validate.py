from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, RequestConfig

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
        queryset = DocumentFile.objects.filter(stage=STAGES[6])
        self.table = ValidationTable(queryset)
        self.filter = DocumentFileFilter(self.request.GET,
                                         DocumentFile.objects.filter(stage=STAGES[6]))
        self.table = ValidationTable(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)
        # return Batch.objects.filter(is_return_batch=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['table'] = self.table
        context['filter'] = self.filter
        return context


def open_file_for_Validator(request, id):
    file = DocumentFile.objects.get(pk=id)
    table = ValidateQADocTable(DocumentFileDetail.objects.filter(pk=id))
    return render(request, 'qa/documents.html', {'file': file, 'table': table})
