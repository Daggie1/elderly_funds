import django_filters
from .models import DocumentFile, DocumentFileDetail


class DocumentFileFilter(django_filters.FilterSet):
    class Meta:
        model = DocumentFile
        fields = ['file_reference']


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = DocumentFileDetail
        fields = ['document_barcode']
