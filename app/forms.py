from django.forms import ModelForm, Form
from django import forms
from .models import DocumentFileType, DocumentType, DocumentFile


class FileForm(forms.ModelForm):
    class Meta:
        model = DocumentFileType
        fields = ['file_type', 'file_description']


class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = ['document_name', 'document_description']


class DocumentForm(forms.ModelForm):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

    class Meta:
        model = DocumentFile
        fields = ['file_type']
