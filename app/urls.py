from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from .views import DocumentTypeView, search_file, AdminView, edit_file, \
    manage_documents, FileTypeDelete, FileTypeCreate, FileTypeList, DocumentFileCreate, DocumentFileList, \
    DocumentTypeCreate, DocumentTypeList, DocumentUploadView, UploadedDocumentsList, DocumentTranscribe, \
    get_document_and_document_type, pdfrender, UserListView, UserDetailView, UserUpdateView, UserDeleteView, \
    GroupListView, GroupUpdateView, user_create, password_reset, add_group, login, update_document_content, validate_document_content

urlpatterns = [
    path('', AdminView.as_view(), name='home'),

    # file type urls
    path('create_file_type/', FileTypeCreate.as_view(), name='create_file_type'),
    path('list_files_types', FileTypeList.as_view(), name='list_file_types'),
    path('delete_file_type/<str:pk>/delete/', FileTypeDelete.as_view(), name='delete_file_type'),
    # physical file urls
    path('create_file', DocumentFileCreate.as_view(), name='create_document_file'),
    path('list_document_files', DocumentFileList.as_view(), name='list_document_files'),

    # Document Types
    path('create_document_type', DocumentTypeCreate.as_view(), name='create_document_type'),
    path('view_document_types', DocumentTypeList.as_view(), name='list_document_types'),

    # document upload and viewing
    path('upload_document', DocumentUploadView.as_view(), name='upload_document'),
    path('uploaded_documents', UploadedDocumentsList.as_view(), name='uploaded_documents'),


    # transcribe urls
    path('view_docs_in_file/<str:file_reference>', DocumentTranscribe.as_view(), name='view_docs_in_file'),
    path('transcription_lab/<int:doc_id>/<str:file_type>',get_document_and_document_type, name='transcription_lab'),
    path('update_doc_content/<int:doc_id>', update_document_content, name='update_doc_content' ),
    path('validate_doc_content/<int:doc_id>', validate_document_content, name='validate_doc_content'),
    path('search_file', search_file, name='search_file'),
    path('pdf_render', pdfrender, name='pdf_render'),

    # Auth
    path('users/', UserListView.as_view(), name='users.index'),
    path('users/', UserListView.as_view(), name='users.index'),
    path('users/create/', user_create, name='users.create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='users.detail'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user.update'),
    path('users/password_reset/', password_reset, name='user.changepass'),

    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user.delete'),
    # groups
    path('roles/', GroupListView.as_view(), name='groups.index'),
    path('roles/create/', add_group, name='roles.create'),
    path('roles/update/<int:pk>/', GroupUpdateView.as_view(), name='groups.update'),
    #
    path('login/', login, name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),

]

