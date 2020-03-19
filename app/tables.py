import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import DocumentFile


class DocumentFileTable(tables.Table):
    class Meta:
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference","file_type","file_status","captured_by","file_barcode","created_on","edit")

    edit = TemplateColumn(template_name='app/file_action_column.html')

