import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import DocumentFile, DocumentFileDetail, Batch


class BatchTable(tables.Table):
    class Meta:
        model = Batch
        template_name = "django_tables2/bootstrap.html"
        fields = ("batch_no", "name", "created_on", "state")

    actions = TemplateColumn(template_name='batch/view_column.html')

class DocumentFileTable(tables.Table):
    class Meta:
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "file_status", "captured_by", "file_barcode", "created_on")

    action = TemplateColumn(template_name='file/view_column.html')
    # transcribe = TemplateColumn(template_name='app/document_action_column.html')


class DocumentTable(tables.Table):
    class Meta:
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference_id", "document_barcode", "document_name_id", "document_file_path")

    Transcribe = TemplateColumn(template_name='app/document_transcribe.html')
    validate = TemplateColumn(template_name='app/inspect_document_column.html')
