from django.forms import Form
from django import forms
from django_jsonforms.forms import JSONSchemaField
from .models import DocumentFileType, DocumentType, DocumentFile


class FileForm(forms.ModelForm):
    class Meta:
        model = DocumentFileType
        fields = ['file_type', 'file_description']


class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = ['document_name', 'document_description']


class DocumentForm(forms.Form):
    file_barcode = forms.CharField(label="Read Document Barcode", max_length=40)
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class BirthCertificateForm(Form):
    name = forms.CharField(label="Full Names")
    fathers_name = forms.CharField(label="Father's Name")
    mothers_name = forms.CharField(label="Mother's Name")
    birth_entry_no = forms.CharField(label="Birth Entry No")
    date_of_birth = forms.CharField(label="date of birth")
    location = forms.CharField(label="District of Birth")
    gender = forms.CharField(label="Gender")


class NationalIDForm(Form):
    id_no = forms.IntegerField(label='ID Card Number')
    full_names = forms.CharField(label='Full Names')
    date_of_birth = forms.DateTimeField(label='Date of Birth')
    gender = forms.Select( choices=['Male', 'Female'])
    district = forms.CharField(label='District')
    division = forms.CharField(label='Division')
    location = forms.CharField(label='Location')
    sub_location = forms.CharField(label='Sub Location')
