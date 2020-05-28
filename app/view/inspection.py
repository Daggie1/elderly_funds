from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, reverse

from django.contrib import messages

from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
import itertools

from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, RequestConfig

from app.filters import DocumentFilter, BatchFilter, DocumentFileFilter
from app.models import DocumentFileDetail, DocumentFile, Batch, Modification, STAGES, STATES
from app.tables import ReceiverTable, ReceiverFiles, AssemblerFiles, AssemblerDocuments, DocumentTable


def receive(request, id=None):
    # make a query
    # documents = DocumentFileDetail.objects.get(pk=id)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        query = request.GET.get('q')
        if query:
            qset = (
                Q(batch_no__icontains=query)
            )
            results = Batch.objects.filter(qset).distinct()
        else:
            results = []
        if id is not None:
            files = DocumentFile.objects.filter(batch=id, stage=STAGES[1]).values('file_barcode', 'file_reference',
                                                                                  'state')
            batch = Batch.objects.get(pk=id)
        else:
            batch = ''
            files = []
    context = {'results': results, 'batch': batch, 'files': list(files)}
    return render(request, 'inspect/receiver.html', context=context)


def inspect(request, id=None):
    # make a query
    # documents = DocumentFileDetail.objects.get(pk=id)
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        query = request.GET.get('q')
        if query:
            qset = (
                Q(file_barcode__icontains=query)
            )
            results = DocumentFile.objects.filter(qset).distinct()
        else:
            results = []
        if id is not None:
            documents = DocumentFileDetail.objects.filter(file_reference=id).values_list('document_barcode', flat=True)
            file = DocumentFile.objects.get(pk=id)

            if file.assigned_to == None:
                returned_object_type = ContentType.objects.get(app_label='app', model='documentfile')
                print(f'returned_obj={returned_object_type}')
                try:
                    file.assigned_to = request.user
                    file.save()
                    Modification.objects.create(object_type=returned_object_type, object_pk=file.pk,
                                                modified_from_state=file.state, by=request.user)

                except AttributeError as e:
                    messages.error(request, 'Something wrong happened')
            else:
                if file.assigned_to != request.user:
                    messages.error(request, "Permission denied")
        else:
            file = ''
            documents = []
    context = {'results': results, 'file': file, 'documents': list(documents)}
    print(documents)
    return render(request, 'inspect/index.html', context=context)


class ReceiveBatch(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = ReceiverTable
    template_name = 'inspect/receiver_batch.html'
    filterset_class = BatchFilter

    def get_queryset(self):
        queryset = Batch.objects.filter(is_return_batch=False, state=STATES[2])
        self.table = ReceiverTable(queryset)
        self.filter = BatchFilter(self.request.GET,
                                     Batch.objects.all())
        self.table = ReceiverTable(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)




class OpenBatchFiles(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = ReceiverFiles
    template_name = 'inspect/receiver_table.html'
    filterset_class = DocumentFileFilter

    def get_queryset(self):
        queryset = DocumentFile.objects.filter(stage=STAGES[1])
        self.table = ReceiverFiles(queryset)
        self.filter = DocumentFilter(self.request.GET,
                                     DocumentFile.objects.filter(pk=self.kwargs['id']))
        self.table = ReceiverFiles(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)
        return queryset

class DessembleFiles(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = AssemblerFiles
    template_name = 'inspect/assembler_files.html'
    filterset_class = DocumentFileFilter

    def get_queryset(self):
        queryset = DocumentFile.objects.filter(stage=STAGES[2])
        self.table = AssemblerFiles(queryset)
        self.filter = DocumentFilter(self.request.GET,
                                     DocumentFile.objects.filter(stage='Assembler'))
        self.table = AssemblerFiles(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)
        return queryset


class DessemblerDocuments(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = AssemblerDocuments
    template_name = 'inspect/assembler_table.html'
    filterset_class = DocumentFilter

    def get_queryset(self):
        queryset = DocumentFileDetail.objects.filter(file_reference=self.kwargs['id'])
        self.table = AssemblerDocuments(queryset)
        self.filter = DocumentFilter(self.request.GET,
                                     DocumentFileDetail.objects.filter(file_reference_id=self.kwargs['id']))
        self.table = DocumentTable(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)
        return queryset

