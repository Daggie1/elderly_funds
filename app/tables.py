import django_tables2 as tables
from django_tables2 import TemplateColumn
from .models import DocumentFile, DocumentFileDetail, Batch


class BatchTable(tables.Table):
    class Meta:
        attrs = {"class":"table table-bordered table-striped"}
        model = Batch
        template_name = "django_tables2/bootstrap4.html"
        fields = ("batch_no", "name", "created_on","created_by", "state","description")
    files = TemplateColumn(template_name='batch/total_column.html')
    actions = TemplateColumn(template_name='batch/view_column.html')


class BatchFileTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "captured_by", "file_barcode", "created_on")

    docs = TemplateColumn(template_name='file/total_column.html')
    action = TemplateColumn(template_name='batch/file_view_column.html')


class BatchDocumentTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap4.html"
        fields = ("file_reference_id", "document_barcode", "document_name_id", "document_file_path")

    actions = TemplateColumn(template_name='app/document_transcribe.html')


class DocumentFileTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "captured_by", "file_barcode", "created_on")

    docs = TemplateColumn(template_name='file/total_column.html')
    action = TemplateColumn(template_name='file/view_column.html')
    # transcribe = TemplateColumn(template_name='app/document_action_column.html')


class DocumentTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap4.html"
        fields = ("file_reference_id", "document_barcode", "document_name_id", "document_file_path")

    actions = TemplateColumn(template_name='app/document_transcribe.html')



class ValidationTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "captured_by", "file_barcode", "created_on")

    docs = TemplateColumn(template_name='file/total_column.html')
    validate = TemplateColumn(template_name='file/view_column.html')


class QaTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "captured_by", "file_barcode", "created_on")

    docs = TemplateColumn(template_name='file/total_column.html')
    action = TemplateColumn(template_name='file/view_column.html')
