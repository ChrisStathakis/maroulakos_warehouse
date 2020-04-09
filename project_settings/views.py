from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.db import models
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.db.models import Sum

from .models import Storage, PaymentMethod
from .tables import StorageTable, PaymentMethodTable
from .forms import StorageForm, PaymentMethodForm

from django_tables2 import RequestConfig


@method_decorator(staff_member_required, name='dispatch')
class HomepageView(TemplateView):
    template_name = 'project_settings/dashboard.html'


@method_decorator(staff_member_required, name='dispatch')
class StorageListView(ListView):
    model = Storage
    template_name = 'project_settings/list_view.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_table = StorageTable(self.object_list)
        RequestConfig(self.request, {'per_page': self.paginate_by}).configure(queryset_table)
        context['queryset_table'] = queryset_table
        context['create_url'] = reverse('settings:storage_create')
        context['back_url'] = reverse('settings:homepage')
        return context


@method_decorator(staff_member_required, name='dispatch')
class StorageCreateView(CreateView):
    template_name = 'project_settings/form_view.html'
    form_class = StorageForm
    model = Storage
    success_url = reverse_lazy('settings:storage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = 'Δημιουργια Χωρου Αποθηκευσης'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Δημιουργηθηκε νέα καταχώρηση')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class StorageUpdateView(UpdateView):
    template_name = 'project_settings/form_view.html'
    form_class = StorageForm
    model = Storage
    success_url = reverse_lazy('settings:storage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = 'Επεξεργασια Χωρου Αποθηκευσης'
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η Επεξεργασια αποθηκευτηκε.')
        return super().form_valid(form)


@staff_member_required
def delete_storage_view(request, pk):
    instance = get_object_or_404(Storage, id=pk)
    try:
        instance.delete()
    except models.ProtectedError:
        messages.warning(request, 'Δεν μπορείτε να το διαγράψετε')
    return redirect(reverse('settings:storage_list'))


@method_decorator(staff_member_required, name='dispatch')
class PaymentMethodListView(ListView):
    model = PaymentMethod
    template_name = 'project_settings/list_view.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_table = StorageTable(self.object_list)
        RequestConfig(self.request, {'per_page': self.paginate_by}).configure(queryset_table)
        context['queryset_table'] = queryset_table
        context['create_url'] = reverse('settings:payment_create')
        context['back_url'] = reverse('settings:homepage')
        return context


@method_decorator(staff_member_required, name='dispatch')
class PaymentMethodCreateView(CreateView):
    template_name = 'project_settings/form_view.html'
    form_class = PaymentMethodForm
    model = PaymentMethod
    success_url = reverse_lazy('settings:payment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = 'Δημιουργια Χωρου Αποθηκευσης'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Δημιουργηθηκε νέα καταχώρηση')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class PaymentMethodUpdateView(UpdateView):
    template_name = 'project_settings/form_view.html'
    form_class = StorageForm
    model = Storage
    success_url = reverse_lazy('settings:payment_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = 'Επεξεργασια Χωρου Αποθηκευσης'
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η Επεξεργασια αποθηκευτηκε.')
        return super().form_valid(form)


@staff_member_required
def delete_payment_view(request, pk):
    instance = get_object_or_404(PaymentMethod, id=pk)
    try:
        instance.delete()
    except models.ProtectedError:
        messages.warning(request, 'Δεν μπορείτε να το διαγράψετε')
    return redirect(reverse('settings:payment_list'))
