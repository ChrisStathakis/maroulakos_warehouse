from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.db.models import Sum

from .models import Storage
from .tables import StorageTable

from django_tables2 import RequestConfig


@method_decorator(staff_member_required, name='dispatch')
class HomepageView(TemplateView):
    template_name = ''


@method_decorator(staff_member_required, name='dispatch')
class StorageListView(ListView):
    model = Storage
    template_name = 'dashboard/list_view.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_table = StorageTable(self.object_list)
        RequestConfig(self.request, {'per_page': self.paginate_by}).configure(queryset_table)
        context['queryset_table'] = queryset_table

        return context
