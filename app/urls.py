from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path

from app.view.batch import BatchListView, create_batch
from app.view.document import DocumentCreate, DocumentView, UploadedDocumentsList
from app.view.document_type import DocumentTypeCreate, DocumentTypeList
from app.view.file import FilesView, DocumentFileCreate, DocumentFileList
from app.view.file_type import FileTypeCreate, FileTypeList
from app.view.scanner import upload_documents_to_file, get_file_to_upload_documents
from app.view.transcribe import get_files_from_storage, update_document_file_detail
from .views import (
    registry_submit, AdminView, FileTypeDelete,
    DocumentTranscribe,
    get_document_and_document_type,
    UserListView, UserDetailView, UserUpdateView,
    UserDeleteView, GroupListView, GroupUpdateView, user_create,
    add_group, login, update_document_content,
    validate_document_content)

urlpatterns = [
    path('', AdminView.as_view(), name='home'),
    #submits
    path('submit/<int:batch_id>', registry_submit, name='submit.registry'),

    # batches
    path('batches/', BatchListView.as_view(), name='batch_index'),
    path('create_batch/',create_batch,name='batch_create'),

    # file type urls
    path('create_file_type/', FileTypeCreate.as_view(), name='create_file_type'),
    path('list_files_types', FileTypeList.as_view(), name='list_file_types'),
    path('delete_file_type/<str:pk>/delete/', FileTypeDelete.as_view(), name='delete_file_type'),

    # physical file urls
    path('batch/<int:batch_id>/files', FilesView.as_view(), name='files.view'),
    path('batch/<int:batch_id>/create_file/', DocumentFileCreate.as_view(), name='create_document_file'),
    path('list_document_files', DocumentFileList.as_view(), name='list_document_files'),

    # Document Types
    path('create_document_type', DocumentTypeCreate.as_view(), name='create_document_type'),
    path('view_document_types', DocumentTypeList.as_view(), name='list_document_types'),

    # document upload and viewing
    path('file/<file_ref_no>/documents', DocumentView.as_view(), name='document.view'),
    path('file/<file_ref_no>/create_document/', DocumentCreate.as_view(), name='document.create'),
    path('uploaded_documents', UploadedDocumentsList.as_view(), name='uploaded_documents'),
    path('files/upload/select',get_file_to_upload_documents, name='get_file_to_upload_documents'),
    path('upload/to/file/<str:file_reference>',upload_documents_to_file, name='upload_document'),


    # transcribe urls
    path('view_docs_in_file/<str:file_reference>', DocumentTranscribe.as_view(), name='view_docs_in_file'),
    path('transcription_lab/<int:doc_id>/<str:file_type>',get_document_and_document_type, name='transcription_lab'),
    path('update_doc_content/<int:doc_id>', update_document_content, name='update_doc_content' ),
    path('validate_doc_content/<int:doc_id>', validate_document_content, name='validate_doc_content'),

    path('file/document/storage/<str:file_reference>', get_files_from_storage, name='get_files_from_storage'),
    path('update/document/<int:document>',update_document_file_detail, name='update_document_file_detail'),

    # Auth
    path('users/', UserListView.as_view(), name='users.index'),
    path('users/', UserListView.as_view(), name='users.index'),
    path('users/create/', user_create, name='users.create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='users.detail'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user.update'),
    path('users/password_reset/', PasswordChangeView.as_view( template_name='reset_password.html'), name='user.changepass'),

    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user.delete'),
    # groups
    path('roles/', GroupListView.as_view(), name='groups.index'),
    path('roles/create/', add_group, name='roles.create'),
    path('roles/update/<int:pk>/', GroupUpdateView.as_view(), name='groups.update'),
    #
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

]

