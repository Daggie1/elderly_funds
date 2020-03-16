from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from .forms import FileForm, DocumentTypeForm, DocumentForm


# Create your views here.

class FileView(View):
    def get(self, request):
        template_name = 'add_file.html'
        form = FileForm()
        return render(request, template_name, {'form': form})

    def post(self, request):
        template_name = 'view_files.html'
        form = FileForm(request.Post)

        if form.is_valid():
            form.save()
            return render(request, template_name)
        else:
            return redirect('add_file')


class DocumentTypeView(View):
    def get(self, request):
        template_name = 'add_document_type.html'
        form = DocumentTypeForm()
        return render(request, template_name, {'form': form})

    def post(self, request):
        pass


class DocumentUpload(View):
    def get(self, request):
        template_name = 'upload_document.html'
        form = DocumentForm()
        return render(request, template_name, {'form':form})

    def post(self):
        pass
