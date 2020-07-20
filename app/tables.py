import itertools

import django_tables2 as tables
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django_tables2 import TemplateColumn, A
from .models import DocumentFile, DocumentFileDetail, Batch, Modification, Stock
from django.urls import reverse


class BatchTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped table-responsive"}
        model = Batch
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "batch_no", "created_on", "created_by", "state", "description")

    files = TemplateColumn(template_name='batch/total_column.html')
    actions = TemplateColumn(template_name='batch/view_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class StockTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped table-responsive"}
        model = Stock
        template_name = "django_tables2/bootstrap4.html"
        fields = ('file_number', 'name', 'nationality', 'cross_reference', 'file_category', 'date_last_correspondence',
                  'date_first_correspondence', 'location_of_file')

    actions = TemplateColumn(template_name='stock/view_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class ReturnBatchTable(tables.Table):
    # transitions = tables.Column(accessor='get_transition_options',verbose_name='Transition')
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped table-responsive"}
        model = Batch
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "batch_no", "created_on", "created_by", "state", "description")

    files = TemplateColumn(template_name='batch/total_column.html')
    actions = TemplateColumn(template_name='batch/view_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class BatchFileTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap4.html"
        fields = (
        "counter", "file_reference", "file_type", "state", "stage", "file_created_by", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    docs = TemplateColumn(template_name='file/total_column.html')
    change_state = TemplateColumn(template_name='batch/file_state_column.html')
    move_stage = TemplateColumn(template_name='batch/file_view_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class BatchDocumentTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference_id", "document_barcode", "state", "document_name_id", "document_file_path")

    actions = TemplateColumn(template_name='app/document_transcribe.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class DocumentFileTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile

        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference", "file_type", "state", "stage", "file_barcode", "created_on")

    docs = TemplateColumn(template_name='file/total_column.html')
    action = TemplateColumn(template_name='file/view_column.html')

    # transcribe = TemplateColumn(template_name='app/document_action_column.html')
    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class EscalatedFileTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        row_attrs = {
            "class": lambda record: "bg-red" if record.flagged else "bg-default"
        }
        model = DocumentFile
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference", "file_type", "state", "file_created_by", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    docs = TemplateColumn(template_name='file/total_column.html')
    action = TemplateColumn(template_name='file/escalated_column.html')

    # transcribe = TemplateColumn(template_name='app/document_action_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class DocumentTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference_id", "document_barcode", "document_file_path")

    actions = TemplateColumn(template_name='app/document_transcribe.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class ValidationTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference", "file_type", "state", "file_created_by", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    docs = TemplateColumn(template_name='file/total_column.html')
    validate = TemplateColumn(template_name='file/validator_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class QaTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference", "file_type", "state", "file_created_by", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    docs = TemplateColumn(template_name='file/total_column.html')

    action = TemplateColumn(template_name='file/qa_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class ScannerTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference", "state", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    docs = TemplateColumn(template_name='file/total_column.html')
    action = TemplateColumn(template_name='file/scan.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class TranscribeTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference", "file_type", "state", "file_created_by", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    transcribe = TemplateColumn(template_name='app/document_action_column.html')
    action = TemplateColumn(template_name='file/view_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class HistoryTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = Modification
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file", "modified_from_stage", "modified_to_stage", "by", "created_at")

    view = TemplateColumn(template_name='file/view_history.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class SpecificFileUserHistoryTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = Modification
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "modified_from_stage", "modified_to_stage", "created_at")

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class AdminTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file", 'file_reference')

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class ValidateQADocTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference_id", "document_barcode", "document_file_path")

    actions = TemplateColumn(template_name='document/inspect.html')

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class ReceiverTable(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped table-responsive"}
        model = Batch
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "batch_no", "created_on", "state", "description")

    files = TemplateColumn(template_name='batch/total_column.html')
    actions = TemplateColumn(template_name='batch/receive_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class ReceiverFiles(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        row_attrs = {
            "class": lambda record: "bg-gradient-cyan" if record.stage == 'Reception' else "bg-default"
        }
        model = DocumentFile
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference", "file_type", "stage", "file_created_by", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    docs = TemplateColumn(template_name='file/total_column.html')
    move_stage = TemplateColumn(template_name='batch/receiver_actions.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class AssemblerFiles(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        row_attrs = {
            "class": lambda record: "bg-gradient-cyan" if record.stage != 'Assembly' else "bg-default"
        }
        template_name = "django_tables2/bootstrap4.html"
        fields = (
        "counter", "file_reference", "file_type", "state", "stage", "file_created_by", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    docs = TemplateColumn(template_name='file/total_column.html')
    move_stage = TemplateColumn(template_name='batch/assembly_column.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class AssemblerDocuments(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFileDetail
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference_id", "file_reference", "document_barcode", "state")

    actions = TemplateColumn(template_name='app/assembler_document_actions.html')

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)


class CompleteFiles(tables.Table):
    counter = tables.Column(empty_values=(), orderable=False)

    class Meta:
        attrs = {"class": "table table-bordered table-striped"}
        model = DocumentFile
        template_name = "django_tables2/bootstrap4.html"
        fields = ("counter", "file_reference", "file_type", "state", "stage", "file_barcode", "created_on")

    def render_file_reference(self, value, record):
        url = reverse('file_details', kwargs={'pk': record.pk})
        return mark_safe(f'<a href="{url}"><strong>{value}</strong></a>')

    docs = TemplateColumn(template_name='file/total_column.html')
    open = TemplateColumn(template_name='file/open_eye.html')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)
