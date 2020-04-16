from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path

from app.view.batch import BatchListView, create_batch,BatchDeleteView
from app.view.document import DocumentCreate, DocumentView, UploadedDocumentsList, create_document
from app.view.document_type import DocumentTypeCreate, DocumentTypeList
from app.view.file import FilesView, DocumentFileCreate, DocumentFileList
from app.view.file_type import FileTypeCreate, FileTypeList
from app.view.scanner import upload_documents_to_file, get_file_to_upload_documents
from app.view.transcribe import get_files_from_storage, update_document_file_detail
from app.view.api import ApiViewSet
from .views import (
    registry_submit, AdminView, FileTypeDelete,request_file,
    DocumentTranscribe,
    get_document_and_document_type,
    UserListView, UserDetailView, UserUpdateView,
    UserDeleteView, GroupListView, GroupUpdateView, user_create, Login,
     add_group, update_document_content,
    validate_document_content,
    registry_batch_submit,receiver_batch_submit,
    file_submit,start_receive,start_scanning,start_qa,start_validate,change_password)




urlpatterns = [
    path('', AdminView.as_view(), name='home'),
    #submits
    path('submit/<int:batch_id>', registry_submit, name='submit.registry'),

    # batches
    path('batches/', BatchListView.as_view(), name='batch_index'),
    path('create_batch/',create_batch,name='batch_create'),
    path('batch/<int:pk>/delete/', BatchDeleteView.as_view(), name='batch_delete'),

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
    path('file/<file_ref_no>/create_document/', create_document, name='document.create'),
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
    path('users/password_reset/<username>', change_password, name='user.changepass'),

    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user.delete'),
    # groups
    path('roles/', GroupListView.as_view(), name='groups.index'),
    path('roles/create/', add_group, name='roles.create'),
    path('roles/update/<int:pk>/', GroupUpdateView.as_view(), name='groups.update'),
    #

    path('login/', Login.as_view(), name='login'),

    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('change_status/<file_ref>/', file_submit, name='file_submit'),

    path('registry_submit_batch/<int:batch_id>/', registry_batch_submit, name='registry_submit_batch'),
    path('receiver_submit_batch/<int:batch_id>/', receiver_batch_submit, name='receiver_submit_batch'),

    path('receive/<int:batch_id>/', start_receive, name='start_receive'),
    path('scan/<file_ref>/', start_scanning, name='start_scan'),
    path('qa/<file_ref>/', start_qa, name='start_qa'),
    path('validate/<file_ref>/', start_validate, name='start_validate'),

    path('request_file', request_file, name='request_file'),

    # api endpoints
    # path('api/v1/',ApiViewSet.as_view(), name='api'),
]

