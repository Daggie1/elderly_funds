import django_tables2 as tables
from django.utils.html import format_html
from django_tables2 import TemplateColumn
from .models import DocumentFile, DocumentFileDetail, Batch, Modification


class BatchTable(tables.Table):
    # transitions = tables.Column(accessor='get_transition_options',verbose_name='Transition')
    class Meta:
        attrs = {"class": "table table-bordered table-striped table-responsive"}
        model = Batch
        template_name = "django_tables2/bootstrap4.html"
        fields = ("batch_no", "created_on", "created_by", "state", "description")

    files = TemplateColumn(template_name='batch/total_column.html')
    actions = TemplateColumn(template_name='batch/view_column.html')


class ReturnBatchTable(tables.Table):
    # transitions = tables.Column(accessor='get_transition_options',verbose_name='Transition')
    class Meta:
        attrs = {"class": "table table-bordered table-striped table-responsive"}
        model = Batch
        template_name = "django_tables2/bootstrap4.html"
        fields = ("batch_no", "created_on", "created_by", "state", "description")

    files = TemplateColumn(template_name='batch/total_column.html')
    actions = TemplateColumn(template_name='batch/view_column.html')


class BatchFileTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "stage", "captured_by", "file_barcode", "created_on")
    def render_file_reference(self, value, record):
        return format_html('<a href="{}" ><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))
    docs = TemplateColumn(template_name='file/total_column.html')
    change_state = TemplateColumn(template_name='batch/file_state_column.html')
    move_stage = TemplateColumn(template_name='batch/file_view_column.html')


class BatchDocumentTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap4.html"
        fields = ("file_reference_id", "document_barcode", "state", "document_name_id", "document_file_path")

    actions = TemplateColumn(template_name='app/document_transcribe.html')


class DocumentFileTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "captured_by", "file_barcode", "created_on")

    docs = TemplateColumn(template_name='file/total_column.html')
    action = TemplateColumn(template_name='file/view_column.html')

    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))
    # transcribe = TemplateColumn(template_name='app/document_action_column.html')


class EscalatedFileTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        row_attrs = {
            "class": lambda record: "bg-red" if record.flagged else "bg-default"
        }
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "captured_by", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))


    docs = TemplateColumn(template_name='file/total_column.html')
    action = TemplateColumn(template_name='file/view_column.html')
    # transcribe = TemplateColumn(template_name='app/document_action_column.html')


class DocumentTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap4.html"
        fields = ("file_reference_id", "document_barcode", "document_file_path")

    actions = TemplateColumn(template_name='app/document_transcribe.html')


class ValidationTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "captured_by", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))

    docs = TemplateColumn(template_name='file/total_column.html')
    validate = TemplateColumn(template_name='file/validator_column.html')


class QaTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "captured_by", "file_barcode", "created_on")
    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))
    docs = TemplateColumn(template_name='file/total_column.html')

    action = TemplateColumn(template_name='file/qa_column.html')


class ScannerTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "state", "file_barcode", "created_on")
    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))
    docs = TemplateColumn(template_name='file/total_column.html')
    action = TemplateColumn(template_name='file/scan.html')


class TranscribeTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "captured_by", "file_barcode", "created_on")
    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))
    docs = TemplateColumn(template_name='file/total_column.html')
    transcribe = TemplateColumn(template_name='app/document_action_column.html')


class HistoryTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = Modification
        template_name = "django_tables2/bootstrap.html"
        fields = ("file", "modified_from_stage", "modified_to_stage", "by", "created_at")

    view = TemplateColumn(template_name='file/view_history.html')


class SpecificFileUserHistoryTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = Modification
        template_name = "django_tables2/bootstrap.html"
        fields = ("modified_from_stage", "modified_to_stage", "created_at")


class AdminTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file",)
    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))
    actions = TemplateColumn(template_name='file/view_history.html')


class ValidateQADocTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference_id", "document_barcode", "document_file_path")

    actions = TemplateColumn(template_name='document/inspect.html')


class ReceiverTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped table-responsive"}
        model = Batch
        template_name = "django_tables2/bootstrap4.html"
        fields = ("batch_no", "created_on", "state", "description")

    files = TemplateColumn(template_name='batch/total_column.html')
    actions = TemplateColumn(template_name='batch/receive_column.html')


class ReceiverFiles(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "stage", "captured_by", "file_barcode", "created_on")
    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))
    docs = TemplateColumn(template_name='file/total_column.html')
    change_state = TemplateColumn(template_name='batch/file_state_column.html')
    move_stage = TemplateColumn(template_name='batch/file_view_column.html')


class AssemblerFiles(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap.html"
        fields = ("file_reference", "file_type", "state", "stage", "captured_by", "file_barcode", "created_on")
    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))
    docs = TemplateColumn(template_name='file/total_column.html')
    change_state = TemplateColumn(template_name='batch/file_state_column.html')
    move_stage = TemplateColumn(template_name='batch/file_view_column.html')


class AssemblerDocuments(tables.Table):
    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap4.html"
        fields = ("file_reference_id", "document_barcode", "state", "document_name_id", "document_file_path")
    def render_file_reference(self, value, record):
        return format_html('<a href="{}"><strong>{}</strong></a>'.format('file_details/{}'.format(record.pk), value))
    actions = TemplateColumn(template_name='app/document_transcribe.html')
