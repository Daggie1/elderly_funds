from django.urls import path, re_path

from .views import FileView, DocumentTypeView, DocumentUpload

urlpatterns = [
    path('', FileView.as_view(), name='add_file'),
    path('add_document_type/', DocumentTypeView.as_view(), name='add_doc_type'),
    path('upload_document/', DocumentUpload.as_view(), name='upload_document')
]
