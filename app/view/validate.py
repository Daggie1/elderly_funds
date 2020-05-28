from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from app.filters import DocumentFileFilter
from app.models import DocumentFile
from app.tables import ValidationTable
from app.models import STAGES

class ValidateFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'

    table_class = ValidationTable
    template_name = 'qa/index.html'

    def get_queryset(self):
        return DocumentFile.objects.filter(stage=STAGES[6]).filter(
            flagged=True,
            assigned_to=self.request.user)

    filterset_class = DocumentFileFilter
