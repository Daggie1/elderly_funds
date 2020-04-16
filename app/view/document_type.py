from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.base import View

from app.forms import DocumentTypeForm
from app.models import DocumentType


class DocumentTypeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'app.add_documenttype'
    form_class = DocumentTypeForm
    success_message = 'Added created successfully'
    template_name = 'add_document_type.html'
    success_url = reverse_lazy('list_document_types')


class DocumentTypeList(LoginRequiredMixin, ListView):
    permission_required = 'app.view_documenttype'
    model = DocumentType
    context_object_name = 'documents'
    template_name = 'document_types.html'


class DocumentTypeView(LoginRequiredMixin, SuccessMessageMixin, View):
    permission_required = 'app.view_documenttype'
    success_message = 'Added created successfully'

    def get(self, request):
        template_name = 'add_document_type.html'
        form = DocumentTypeForm()
        return render(request, template_name, {'form': form})

    def post(self, request):
        pass
