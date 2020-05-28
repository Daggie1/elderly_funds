from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path, re_path


from .views import (
    registry_submit, AdminView, FileTypeDelete,request_file,
    DocumentTranscribe,
    get_document_and_document_type,
    UserListView, UserDetailView, UserUpdateView,
    UserDeleteView, GroupListView, GroupUpdateView, user_create, Login,
     add_group, update_document_content,
    validate_document_content,
    receiver_batch_submit,
    start_scanning,start_qa,start_validate,change_password)
from .view.user import reset_default_password
from app.view.file import (
                            FilesView, DocumentFileCreate, DocumentFileList,
                            RejectedDocumentFileList,FileDeleteView,FileUpdateView)
from .view.registry import (registry_submit_to_receiver, change_file_status_to_accept, change_file_status_to_accept_ajax,
                            change_file_status_to_reject,change_document_status_to_accept,
                            change_document_status_to_reject, return_rectified_file)
from .view.receiver import select_file
from app.view.batch import BatchListView, create_batch,BatchDeleteView, BatchFilesView, BatchDocumentsView, ReturnBatchListView,BatchUpdateView
from app.view.document import DocumentDeleteView, DocumentView, UploadedDocumentsList, create_document
from app.view.document_type import DocumentTypeCreate, DocumentTypeList

from app.view.file_type import FileTypeCreate, FileTypeList
from app.view.scanner import upload_documents_to_file, ScannerTableView, delete_document
from app.view.transcribe import get_files_from_storage, update_document_file_detail, TranscribeFiles
from app.view.user import profile,admin_check_user
from .view.report import report,send_report_message
from app.view.inspection import  inspect, receive, ReceiveBatch, OpenBatchFiles, DessembleFiles, DessemblerDocuments
from app.view.qa import  QaFileList, open_file_for_qa
from app.view.validate import ValidateFileList

from app.view.states_methods import update_state_batch,update_state_file,update_state_document
from app.view.stages_methods import update_stage_file
from app.view.file_history import (get_file_history,get_each_user_history,
    get_loggedin_user_history,user_specific_file_history,file_details,assign_file)
from app.view.escalations import RejectedDocumentFileList

urlpatterns = [
    path('', report, name='home'),


    # batches
    path('batches/', BatchListView.as_view(), name='batch_index'),
    path('return/batches/', ReturnBatchListView.as_view(), name='batch_return'),
    path('create_batch/',create_batch,name='batch_create'),
    path('delete_batch/<int:pk>/', BatchDeleteView.as_view(), name='batch_delete'),
    path('edit_batch/<int:pk>/', BatchUpdateView.as_view(), name='batch_edit'),
    path('view/batch/<int:pk>/files/', BatchFilesView.as_view(), name='batch_files' ),
    path('view/batch/<str:file_reference>/documents/', BatchDocumentsView.as_view(), name='batch_documents'),

    # file type urls
    path('create/file_type/', FileTypeCreate.as_view(), name='create_file_type'),
    path('list_files_types', FileTypeList.as_view(), name='list_file_types'),
    path('delete_file_type/<str:pk>/delete/', FileTypeDelete.as_view(), name='delete_file_type'),

    # physical file urls
    path('batch/<int:batch_id>/files', FilesView.as_view(), name='files.view'),
    path('batch/<int:batch_id>/create/file/', DocumentFileCreate.as_view(), name='create_document_file'),
    path('list/document/files', DocumentFileList.as_view(), name='list_document_files'),
    path('list/transcribe/files', TranscribeFiles.as_view(), name='list_transcribe_files'),
    path('list_of_escalated_document_files', RejectedDocumentFileList.as_view(), name='rejected_list_document_files'),
    path('delete_file/<pk>/', FileDeleteView.as_view(), name='file_delete'),
    path('delete_edit/<pk>/', FileUpdateView.as_view(), name='file_edit'),

    # Document Types
    path('create/document/type', DocumentTypeCreate.as_view(), name='create_document_type'),
    path('view/document/types', DocumentTypeList.as_view(), name='list_document_types'),

    # document upload and viewing
    path('file/<file_ref_no>/documents', DocumentView.as_view(), name='document.view'),
    path('file/<file_ref_no>/create_document/', create_document, name='document.create'),
    path('uploaded_documents', UploadedDocumentsList.as_view(), name='uploaded_documents'),
    path('files/upload/select',ScannerTableView.as_view(), name='get_file_to_upload_documents'),
    path('upload/to/file/<str:file_reference>',upload_documents_to_file, name='upload_document'),
    path('delete/uploaded/pdf/<int:id>',delete_document, name='delete_pdf'),
    path('delete_document/<pk>/', DocumentDeleteView.as_view(), name='document_delete'),


    # transcribe urls
    path('view_docs_in_file/<str:file_reference>', DocumentTranscribe.as_view(), name='view_docs_in_file'),
    path('transcription/lab/<int:doc_id>/<str:file_type>',get_document_and_document_type, name='transcription_lab'),
    path('update_doc_content/<int:doc_id>', update_document_content, name='update_doc_content' ),
    path('validate/doc/content/<int:doc_id>', validate_document_content, name='validate_doc_content'),

    path('file/document/storage/<str:file_reference>', get_files_from_storage, name='get_files_from_storage'),
    path('update/document/<int:document>',update_document_file_detail, name='update_document_file_detail'),

    # Auth
    path('users/', UserListView.as_view(), name='users.index'),
    path('users/', UserListView.as_view(), name='users.index'),
    path('users/create/', user_create, name='users.create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='users.detail'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user.update'),
    path('change_password/<username>', change_password, name='user.changepass'),

    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user.delete'),
    # groups
    path('roles/', GroupListView.as_view(), name='groups.index'),
    path('roles/create/', add_group, name='roles.create'),
    path('roles/update/<int:pk>/', GroupUpdateView.as_view(), name='groups.update'),
    #

    path('login/', Login.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('accept_file/<pk>/', change_file_status_to_accept, name='change_file_status_to_accept'),
    re_path(r'^accept_file/ajax/(?P<pk>\w+)/$', change_file_status_to_accept_ajax, name='change_file_status_to_accept_ajax'),
    path('reject_file/<pk>/', change_file_status_to_reject, name='change_file_status_to_reject'),
    path('accept_document/<pk>/', change_document_status_to_accept, name='change_document_status_to_accept'),
    path('reject_document/<pk>/', change_document_status_to_reject, name='change_document_status_to_reject'),
    path('return_rectified_file/<pk>/', return_rectified_file, name='return_rectified_file'),

    path('registry_submit_batch/<int:batch_id>/', registry_submit_to_receiver, name='registry_submit_batch'),
    path('receiver_submit_batch/<int:batch_id>/', receiver_batch_submit, name='receiver_submit_batch'),

    path('select_file/<pk>/', select_file, name='select_file'),
    path('scan/<file_ref>/', start_scanning, name='start_scan'),
    path('qa/<file_ref>/', start_qa, name='start_qa'),
    path('validate/<file_ref>/', start_validate, name='start_validate'),

    path('request_file', request_file, name='request_file'),

    path('profile/', profile, name='profile'),
    path('reset_default_password', reset_default_password, name='reset_default_password'),
    path('check_user<int:pk>', admin_check_user, name='admin_check_user'),
    # api endpoints
    # path('api/v1/',ApiViewSet.as_view(), name='api'),

    # run file and document inspection
    # re_path(r'^inspect/file/$', inspect, name='inspect'),
    # re_path(r'^inspect/file/(?P<id>\w+)/$', inspect, name='inspect'),
    # re_path(r'^receive/batch/$', receive, name='receive'),
    # re_path(r'^receive/batch/(?P<id>\w+)/$', receive, name='receive'),

    re_path(r'^inspect/file/$', DessembleFiles.as_view(), name='inspect'),
    re_path(r'^inspect/file/(?P<id>\w+)/$', DessemblerDocuments.as_view(), name='inspect'),
    re_path(r'^receive/batch/$', ReceiveBatch.as_view(), name='receive'),
    re_path(r'^receive/batch/(?P<id>\w+)/$', OpenBatchFiles.as_view(), name='receive'),

    #quality assuarance link
    path('quality/files/', QaFileList.as_view(), name='quality'),
    path('validate/document/files', ValidateFileList.as_view(), name='validation'),


    #
    #stage and states urls
    #
    path('update_batch_state/<pk>/<action>/', update_state_batch,name='update_state_batch'),
    path('update_file_state/<pk>/<action>/', update_state_file,name='update_state_file'),
    path('update_document_state/<pk>/<action>/', update_state_document,name='update_document_batch'),

    #stage url

    path('update_file_stage/<pk>/<action>/', update_stage_file,name='update_stage_file'),

    #get file history

    path('file_history/<pk>/',get_file_history,name='file_history'),

    #get logged user history
    path('my/history/',get_loggedin_user_history,name='logged_in_user_history'),
    #user specific file history
    path('history_for_file/<pk>',user_specific_file_history,name='user_specific_file_history'),

#get  user history
    path('user/<pk>',get_each_user_history,name='get_user_history'),


#get escalated files
    path('user/escalated/files',RejectedDocumentFileList.as_view(), name='my_escalated_files'),

    #file details

    path('file_details/<pk>',file_details, name='file_details'),

#file details

    path('assign_file/<pk>',assign_file, name='file_assign'),

    # open files for qa
    path('file/qa/open/<int:id>', open_file_for_qa, name='open_qa_file'),

    #send a report message
    path('send/report/',send_report_message, name='chat'),
]

