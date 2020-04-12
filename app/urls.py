from django.contrib.auth.views import LogoutView,PasswordChangeView
from django.urls import path, re_path
from app.view.scanner import upload_documents_to_file,get_file_to_upload_documents
from app.view.transcribe import get_files_from_storage

from .views import (
    BatchListView, create_batch, batch_submit, FilesView, request_file, RequestersFilesView,
    DocumentCreate, DocumentView, search_file, AdminView, edit_file,
    manage_documents, FileTypeDelete, FileTypeCreate,
    FileTypeList, DocumentFileCreate, DocumentFileList,
    DocumentTypeCreate, DocumentTypeList, DocumentUploadView,
    UploadedDocumentsList, DocumentTranscribe,
    get_document_and_document_type, pdfrender,
    UserListView, UserDetailView, UserUpdateView,
    UserDeleteView, GroupListView, GroupUpdateView, user_create, Login, change_password,
    password_reset, add_group, update_document_content,
    validate_document_content, file_submit,start_receive,start_scanning,start_qa,start_validate,abort)

urlpatterns = [
    path('', AdminView.as_view(), name='home'),
    #submits
    path('submit/<int:batch_id>', batch_submit, name='submit.registry'),

    # request file
    path('file_request',request_file,name='file.request'),

    # batches
    path('batches/', BatchListView.as_view(), name='batch.index'),
    path('create_batch/',create_batch,name='batch.create'),

    # file type urls
    path('create_file_type/', FileTypeCreate.as_view(), name='create_file_type'),
    path('list_files_types', FileTypeList.as_view(), name='list_file_types'),
    path('delete_file_type/<str:pk>/delete/', FileTypeDelete.as_view(), name='delete_file_type'),

    # physical file urls
    path('batch/<int:batch_id>/files', FilesView.as_view(), name='files.view'),
    path('batch/<int:batch_id>/create_file/', DocumentFileCreate.as_view(), name='create_document_file'),
    path('myfiles/', RequestersFilesView.as_view(), name='file.myfiles'),
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
    path('search_file', search_file, name='search_file'),
    path('pdf_render', pdfrender, name='pdf_render'),

    path('file/document/storage/<str:file_reference>', get_files_from_storage, name='get_files_from_storage'),

    # Auth
    path('users/', UserListView.as_view(), name='users.index'),
    path('users/', UserListView.as_view(), name='users.index'),
    path('users/create/', user_create, name='users.create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='users.detail'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user.update'),
    path('users/password_change/<str:username>', change_password, name='user.changepass'),

    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user.delete'),
    # groups
    path('roles/', GroupListView.as_view(), name='groups.index'),
    path('roles/create/', add_group, name='roles.create'),
    path('roles/update/<int:pk>/', GroupUpdateView.as_view(), name='groups.update'),
    #
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('abort',abort ,name='abort'),

    path('change_status/<file_ref>/', file_submit, name='file_submit'),

    path('receive/<int:batch_id>/', start_receive, name='start_receive'),
    path('scan/<file_ref>/', start_scanning, name='start_scan'),
    path('qa/<file_ref>/', start_qa, name='start_qa'),
    path('validate/<file_ref>/', start_validate, name='start_validate'),

]

