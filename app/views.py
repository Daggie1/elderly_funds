from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from .forms import testForm


# Create your views here.


def create_file(request):
    json = {'a': 1,
            'b': 2,
            'c': 3,
            'd': 4}
    form = testForm()
    return render(request, 'base.html', {'form': form})


class UploadDocument():
    pass


class QualityAssurance():
    pass


class ValidateDocument():
    pass


class ReadBarCode():
    pass
