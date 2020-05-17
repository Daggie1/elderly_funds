
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django.db.models import Q
from django.urls import reverse_lazy

from django.utils import timezone
from django.views.generic import ListView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from app.filters import DocumentFileFilter
from app.models import DocumentFile, STAGES,STATES
from app.tables import DocumentFileTable


class DocumentFileCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documentfile'
    success_message = 'Added created successfully'
    model = DocumentFile
    template_name = 'file/create.html'
    fields = ['file_reference', 'file_type', 'file_barcode']





    def form_valid(self, form):
        form.instance.file_created_by = self.request.user
        form.instance.state_id = 300
        form.instance.batch_id = self.kwargs['batch_id']
        # file=form.save()
        # print(file.file_reference)
        return super().form_valid(form)
            # reverse_lazy('document.view', kwargrs={'file_ref_no': file.file_reference})


class FilesView(LoginRequiredMixin,  SingleTableMixin, FilterView):
    template_name = 'file/index.html'
    table_class = DocumentFileTable
    def get_context_data(self,  **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['batch_id']=int(self.kwargs['batch_id'])
        print(context)
        return context

    def get_queryset(self):
        if self.request.user.has_perm('app.can_register_batch'):
            return DocumentFile.objects.filter(batch_id=int(self.kwargs['batch_id']))
        elif self.request.user.has_perm('app.can_receive_file'):



            q1 = DocumentFile.objects.filter(state_id = 301,
                                             batch_id=int(self.kwargs['batch_id']),
                                               assigned_to = self.request.user)
            q2 = DocumentFile.objects.filter(state_id = 301,
                                             batch_id=int(self.kwargs['batch_id']),
                                               assigned_to = None)
            return q1.union(q2)


    filterset_class = DocumentFileFilter
    # def get(self, request, *args, **kwargs):
    #     batch_id = kwargs['batch_id']
    #     files = DocumentFile.objects.filter(batch=Batch.objects.get(pk=batch_id))
    #
    #
    #     return render(request, 'file/index.html', {
    #         'object_list': files,
    #         'batch_id': batch_id
    #     })


class DocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_documentfile'

    table_class = DocumentFileTable
    template_name = 'view_document_files.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return DocumentFile.objects.all()
        elif self.request.user.has_perm('app.can_create_batch'):
            return DocumentFile.objects.filter(stage=[0]).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_receive_file'):
            return DocumentFile.objects.filter(stage=[1]).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_disassemble_file'):
            return DocumentFile.objects.filter(stage=[2]).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        elif self.request.user.has_perm('app.can_scan_file'):

         return DocumentFile.objects.filter(stage=[3]).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))


        elif self.request.user.has_perm('app.can_transcribe_file'):


            return DocumentFile.objects.filter(stage=[4]).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))

        elif self.request.user.has_perm('app.can_qa_file'):
            return DocumentFile.objects.filter(stage=[5]).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))

        elif self.request.user.has_perm('app.can_validate_file'):
            return DocumentFile.objects.filter(stage=[6]).filter(Q(assigned_to=self.request.user) | Q(state=STATES[4]))
        else:
            return DocumentFile.objects.none()
    filterset_class = DocumentFileFilter


class RejectedDocumentFileList(LoginRequiredMixin, SingleTableMixin, FilterView):

    table_class = DocumentFileTable
    template_name = 'file/rejected_file_documents_list.html'

    def get_queryset(self):

        if self.request.user.is_superuser:
            return DocumentFile.objects.DocumentFile.objects.filter(
        flagged=True)
        elif self.request.user.has_perm('app.can_create_batch'):
            return DocumentFile.objects.filter(flagged=True).filter(
                                                stage=[0],
                                                assigned_to=self.request.user)
        elif self.request.user.has_perm('app.can_receive_file'):
            return DocumentFile.objects.filter(flagged=True).filter(
                                                stage=[1],
                                                assigned_to=self.request.user)
        elif self.request.user.has_perm('app.can_disassemble_file'):
            return DocumentFile.objects.filter(flagged=True).filter(
                                                stage=[2],
                                                assigned_to=self.request.user)
        elif self.request.user.has_perm('app.can_scan_file'):

            return DocumentFile.objects.filter(flagged=True).filter(
                                                stage=[3],
                                                assigned_to=self.request.user)


        elif self.request.user.has_perm('app.can_transcribe_file'):

            return DocumentFile.objects.filter(flagged=True).filter(
                                                stage=[4],
                                                assigned_to=self.request.user)

        elif self.request.user.has_perm('app.can_qa_file'):
            return DocumentFile.objects.filter(flagged=True).filter(
                                                stage=[5],
                                                assigned_to=self.request.user)

        elif self.request.user.has_perm('app.can_validate_file'):
            return DocumentFile.objects.filter(flagged=True).filter(
                                                stage=[6],
                                                assigned_to=self.request.user)
        else:
            return DocumentFile.objects.none()
    filterset_class = DocumentFileFilter

class FileDeleteView(LoginRequiredMixin,SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = DocumentFile
    success_url = reverse_lazy('list_document_files')
    success_message = 'File Deleted Successfully'
    template_name ='file/delete_confirm.html'

    def test_func(self):
        batch = self.get_object()
        if self.request.user.has_perm('app.can_register_batch'):
            return True
        return False