from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, RequestConfig

from app.filters import StockFilter
from app.forms import StockForm
from app.models import Stock
from app.tables import StockTable


class StockListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class = StockTable
    template_name = 'stock/index.html'
    filterset_class = StockFilter

    def get_queryset(self):
        queryset = Stock.objects.all()
        self.table = StockTable(queryset)
        self.filter = StockFilter(self.request.GET,
                                  Stock.objects.all())
        self.table = StockTable(self.filter.qs)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(self.table)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['table'] = self.table
        context['filter'] = self.filter
        return context


class StockUpdateView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Stock
    fields = ['file_number', 'name', 'nationality', 'cross_reference', 'file_category', 'date_last_correspondence',
              'date_first_correspondence', 'location_of_file']
    template_name = 'stock/create.html'
    success_message = 'Record updated successfully'

    def form_valid(self, form):
        return super().form_valid(form)


@login_required
def create_stock(request):
    if request.method == 'POST':
        form = StockForm(data=request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, f" File Recorded successfully")

                return redirect('stock_index')

            except AttributeError as e:
                print(e)
                messages.error(request, ' something wrong happened while adding batch')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = StockForm()
    return render(request, 'stock/create.html', {'form': form})
