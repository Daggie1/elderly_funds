from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django_tables2 import SingleTableMixin

from app.forms import BatchCreationForm
from app.models import Batch
from app.tables import BatchTable


class BatchListView(LoginRequiredMixin,SingleTableMixin, ListView):
    permission_required = 'app.view_batch'
    model = Batch
    template_name = 'batch/index.html'
    table_class = BatchTable



@login_required
def create_batch(request):
    form = BatchCreationForm(data=request.POST)
    if form.is_valid():
        form.save()
        batch = Batch.objects.get(batch_no=form.cleaned_data.get('batch_no'))
        batch.refresh_from_db()
        batch.created_by = request.user
        batch.save()
        messages.success(request, f"Created successfully")
        for batch in Batch.objects.all():
            print(f'batch: {batch.batch_no} name:{batch.name} by:{batch.created_by}')
        return redirect('batch_index')

    else:
        form = BatchCreationForm()
    return render(request, 'batch/create.html', {'form': form})