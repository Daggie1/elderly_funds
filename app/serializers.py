from .models import DocumentFileDetail
from rest_framework import serializers


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DocumentFileDetail
        fields = ['document_content']
