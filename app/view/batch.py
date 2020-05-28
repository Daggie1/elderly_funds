from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django_filters.views import FilterView
from django.http import HttpResponseRedirect
from django_tables2 import SingleTableMixin, RequestConfig
from django.urls import reverse, reverse_lazy

from app.forms import BatchCreationForm
from app.models import Batch, DocumentFile, DocumentFileDetail, STATES
from app.tables import BatchTable, DocumentFileTable, BatchDocumentTable, DocumentTable, BatchFileTable, \
    ReturnBatchTable
from app.filters import BatchFilter, DocumentFileFilter, DocumentFilter
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DeleteView
)

# TODO remove restriction of quering batch
class BatchListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_batch'
    table_class = BatchTable
    template_name = 'batch/index.html'
    filterset_class = BatchFilter

    def get_queryset(self):

        if self.request.user.has_perm('app.can_register_batch'):
            return Batch.objects.filter(created_by=self.request.user).filter(
                state__in=[STATES[0], STATES[1], STATES[2]])
        elif self.request.user.has_perm('app.can_receive_file'):
            return Batch.objects.filter(is_return_batch=True).filter(created_by=self.request.user).filter(
                state__in=[STATES[0], STATES[1], STATES[2]])
        else:
            return Batch.objects.none()


class ReturnBatchListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_batch'
    table_class = ReturnBatchTable
    template_name = 'batch/return_batch.html'
    filterset_class = BatchFilter

    def get_queryset(self):
        if self.request.user.has_perm('app.can_receive_file'):
            return Batch.objects.filter(is_return_batch=True)
        else:
            return Batch.objects.none()


@login_required
def create_batch(request):
    if request.method == 'POST':
        form = BatchCreationForm(data=request.POST)

        if form.is_valid():
            try:
                batch = Batch.objects.create(batch_no=form.cleaned_data.get('batch_no'),
                                             description=form.cleaned_data.get('description'),
                                             created_by=request.user,
                                             is_return_batch=False)
                batch.save()
                messages.success(request, f" Batch Created successfully")

                # return redirect(reverse('files.view', kwargs={'batch_id': batch.id}))
                return redirect('batch_index')
            except AttributeError as e:
                print(e)
                messages.error(request, ' something wrong happened while adding batch')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = BatchCreationForm()
    return render(request, 'batch/create.html', {'form': form})


class BatchDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    model = Batch
    success_url = reverse_lazy('batch_index')
    success_message = 'Batch Deleted Successfully'
    template_name = 'batch/delete_confirm.html'

    def test_func(self):
        batch = self.get_object()
        if self.request.user.has_perm('app.can_register_batch'):
            return True
        return False


class BatchFilesView(LoginRequiredMixin, SingleTableMixin, FilterView):
    template_name = 'batch/filetable.html'
    table_class = BatchFileTable

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['batch_id'] = int(self.kwargs['batch_id'])
        return context

    def get_queryset(self):
        if self.request.user.has_perm('app.can_register_batch'):
            return DocumentFile.objects.filter(batch_id=int(self.kwargs['batch_id']))
        elif self.request.user.has_perm('app.can_receive_file'):

            q1 = DocumentFile.objects.filter(
                                             batch_id=int(self.kwargs['batch_id']),
                                             assigned_to=self.request.user)
            q2 = DocumentFile.objects.filter(
                                             batch_id=int(self.kwargs['batch_id']),
                                             assigned_to=None)
            return q1.union(q2)

    filterset_class = DocumentFileFilter


class BatchDocumentsView(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.add_documentfiledetail'
    table_class = BatchDocumentTable
    template_name = 'file_documents_list.html'
    filterset_class = DocumentFilter

    def get_queryset(self):
        queryset = DocumentFileDetail.objects.filter(file_reference_id=self.kwargs['file_reference'])
        self.table = BatchDocumentTable(queryset)
        self.filter = DocumentFilter(self.request.GET,
                                     DocumentFileDetail.objects.filter(file_reference_id=self.kwargs['file_reference']))
        self.table = BatchDocumentTable(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['table'] = self.table
        context['filter'] = self.filter

        file = get_file(self.request, self.kwargs['file_reference'])
        print(f'at context{file}')

        context['file_ref_no'] = self.kwargs['file_reference']
        return context


def get_file(request, file_ref=None):
    if not file_ref == None:
        file = DocumentFile.objects.get(pk=file_ref)

        print(f'file ={file}')
        if file:
            print(f'has perms to access file {file}')
            return file

        elif request.user.has_perm("app.can_register_batch"):
            return file
    return None
