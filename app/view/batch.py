from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django_filters.views import FilterView

from django_tables2 import SingleTableMixin, RequestConfig
from django.urls import reverse, reverse_lazy

from app.forms import BatchCreationForm
from app.models import Batch, DocumentState
from app.tables import BatchTable
from app.filters import BatchFilter
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DeleteView
)


class BatchListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'app.view_batch'
    template_name = 'batch/index.html'

    table_class = BatchTable

    def get_queryset(self):
        if self.request.user.has_perm('app.can_register_batch'):
            return Batch.objects.filter(state_id=300)
        elif self.request.user.has_perm('app.can_receive_batch'):
            return Batch.objects.filter(state_id=301)


@login_required
def create_batch(request):
    if request.method == 'POST':
        form = BatchCreationForm(data=request.POST)
        if form.is_valid():
            batch = form.save()
            batch.refresh_from_db()
            batch.created_by = request.user
            batch.state = DocumentState.objects.get(pk=300)
            batch.save()
            messages.success(request, f"Created successfully")

            return redirect(reverse('files.view', kwargs={'batch_id': batch.id}))

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
        if self.request.user == batch.created_by:
            return True
        return False
