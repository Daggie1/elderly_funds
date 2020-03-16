from django.forms import ModelForm, Form
from django import forms
from .models import TestJsonFields


class testForm(Form):

    class Meta:
        model = TestJsonFields
        fields = ['details']
