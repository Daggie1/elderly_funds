import django_filters
from .models import DocumentFile


class DocumentFileFilter(django_filters.FilterSet):
    class Meta:
        model = DocumentFile
        fields = ['file_reference']
