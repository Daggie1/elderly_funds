import django_filters
from .models import DocumentFile, DocumentFileDetail, Batch, Stock


class DocumentFileFilter(django_filters.FilterSet):
    class Meta:
        model = DocumentFile
        fields = ['file_reference']


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = DocumentFileDetail
        fields = ['document_barcode', 'document_type']


class BatchFilter(django_filters.FilterSet):
    class Meta:
        model = Batch
        fields = ['batch_no', 'description']


class StockFilter(django_filters.FilterSet):
    class Meta:
        model = Stock
        fields = ['name', 'file_number', 'location_of_file']
