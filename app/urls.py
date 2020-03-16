from django.urls import path, re_path

from .views import create_file

urlpatterns = [
    path('',create_file, name='add_file')
]