from django.forms import Form, SelectMultiple
from django import forms
from django_jsonforms.forms import JSONSchemaField
from .models import DocumentFileType, DocumentType, DocumentFile, Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group


class FileContentForm(Form):
    schema = None

    json = JSONSchemaField(schema=schema, options={"theme": "bootstrap3"}, ajax=True)


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
    gender = forms.Select(choices=['Male', 'Female'])
    district = forms.CharField(label='District')
    division = forms.CharField(label='Division')
    location = forms.CharField(label='Location')
    sub_location = forms.CharField(label='Sub Location')


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    class Meta:
        model = User
        fields = ['username', 'email', 'groups']
        widgets = {'groups': SelectMultiple(attrs={'required': 'true',
                                                        'class': 'form-control select2',
                                                        'data-dropdown-css-class': 'select2-primary',
                                                        'multiple': 'multiple',
                                                        'data-placeholder': 'Select a State',
                                                        'style': 'width: 100%;'})}


class GroupCreationForm(forms.ModelForm):
    name = forms.TextInput()

    # permissions = forms.SelectMultiple(attrs={'required': u'true',
    #                                           'class': 'select2',
    #                                           'multiple': 'multiple',
    #                                           'data-placeholder': 'Select a State',
    #                                           'style': u"width: 100%;"})

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {'permissions': SelectMultiple(attrs={'required': 'true',
                                                        'class': 'form-control select2',
                                                        'data-dropdown-css-class': 'select2-primary',
                                                        'multiple': 'multiple',
                                                        'data-placeholder': 'Select a State',
                                                        'style': 'width: 100%;'})}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'id_no', 'phone']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class PasswordResetForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
