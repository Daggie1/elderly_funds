from django.urls import path, re_path

from .views import DocumentTypeView, DocumentUpload, search_file, TranscribeDocument, AdminView, edit_file, \
    manage_documents, FileTypeDelete, FileTypeCreate, FileTypeList, DocumentFileCreate, DocumentFileList, DocumentTypeCreate, DocumentTypeList, DocumentUploadView, UploadedDocumentsList

urlpatterns = [
    path('', AdminView.as_view(), name='home'),

    # file type urls
    path('create_file_type/', FileTypeCreate.as_view(), name='create_file_type'),
    path('list_files_types', FileTypeList.as_view(), name='list_file_types'),
    path('delete_file_type/<str:pk>/delete/', FileTypeDelete.as_view(), name='delete_file_type'),
    # physical file urls
    path('create_file', DocumentFileCreate.as_view(), name='create_document_file'),
    path('list_document_files', DocumentFileList.as_view(), name='list_document_files'),

    #Document Types
    path('create_document_type',DocumentTypeCreate.as_view(), name='create_document_type'),
    path('view_document_types', DocumentTypeList.as_view(), name='list_document_types'),

    # document upload and viewing
    path('upload_document', DocumentUploadView.as_view(),name='upload_document'),
    path('uploaded_documents', UploadedDocumentsList.as_view(), name='uploaded_documents'),


    path('add_document_type/', DocumentTypeView.as_view(), name='add_doc_type'),
    path('transcribe/', TranscribeDocument.as_view()),
    path('search_file', search_file, name='search_file'),
]
