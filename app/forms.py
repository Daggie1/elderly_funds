from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.forms.models import ModelForm
from django.forms import Form, SelectMultiple, NumberInput, HiddenInput, TextInput
from django.forms.models import modelformset_factory, formset_factory
from django_jsonforms.forms import JSONSchemaField

from .models import Batch, Filer
from .models import DocumentFileType, DocumentType, Profile, DocumentFileDetail


class FileContentForm(Form):
    schema = None

    json = JSONSchemaField(schema=schema, options={"theme": "bootstrap3"}, ajax=True)


class FileForm(forms.ModelForm):
    class Meta:
        model = DocumentFileType
        fields = ['file_type', 'file_description']


class DocumentTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['document_field_specs'].widget.attrs.update({'id': 'editor_holder'})

    class Meta:
        model = DocumentType
        fields = ['document_name', 'document_description', 'document_field_specs']


class DocumentDetailForm(ModelForm):
    class Meta:
        model = DocumentFileDetail
        fields = ()


DocumentBarCodeFormSet = modelformset_factory(DocumentFileDetail, fields=('document_barcode',), can_delete=False)


class DocForm(forms.Form):
    document_barcode = forms.CharField(max_length=200)


DocFormset = formset_factory(DocForm, extra=1)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(required=True, max_length=25, min_length=8)
    password1 = forms.CharField(widget=HiddenInput())
    password2 = forms.CharField(widget=HiddenInput())
    username = forms.CharField(widget=HiddenInput)
    full_name = forms.CharField(widget=TextInput())
    id_no = forms.IntegerField(widget=NumberInput(attrs={'required': True, }))

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['username'].required = False

    class Meta:
        model = User
        fields = ['full_name', 'email', 'groups', 'phone', 'id_no']
        widgets = {'groups': SelectMultiple(attrs={'required': 'true',
                                                   'class': 'form-control select2',
                                                   'data-dropdown-css-class': 'select2-primary',
                                                   'multiple': 'multiple',
                                                   'data-placeholder': 'Select  Roles',
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
                                                        'data-placeholder': 'Select Permissions',

                                                        'style': 'width: 100%;'})}


class BatchCreationForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_no', 'name']


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


class StorageForm(forms.ModelForm):
    class Meta:
        model = Filer
        fields = ('filepond',)


class ResetPassword(Form):
    username=forms.CharField(max_length=255, required=True)