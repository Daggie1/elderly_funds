from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, RequestConfig

from app.filters import DocumentFileFilter
from app.models import DocumentFile, DocumentFileDetail
from app.tables import QaTable, ValidateQADocTable
from app.models import STAGES


class QaFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'
    filterset_class = DocumentFileFilter
    table_class = QaTable
    template_name = 'qa/index.html'

    def get_queryset(self):
        queryset = DocumentFile.objects.filter(stage=STAGES[5])
        self.table = QaTable(queryset)
        self.filter = DocumentFileFilter(self.request.GET,
                                  DocumentFile.objects.filter(stage=STAGES[5]))
        self.table = QaTable(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)
        # return Batch.objects.filter(is_return_batch=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['table'] = self.table
        context['filter'] = self.filter
        return context

def open_file_for_qa(request, id):
    file = DocumentFile.objects.get(pk=id)
    table = ValidateQADocTable(DocumentFileDetail.objects.filter(file_reference=id))
    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    return render(request, 'qa/documents.html', {'file': file, 'table': table})
