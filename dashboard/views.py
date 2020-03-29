from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.db.models import Sum

from payroll.models import Bill, Payroll
from warehouse.models import Payment
from catalogue.models import Product


@method_decorator(staff_member_required, name='dispatch')
class DashboardHomepageView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills'] = Bill.objects.filter(is_paid=False)[:8]
        context['payroll'] = Payroll.objects.filter(is_paid=False)[:8]
        context['vendor_payments'] = Payment.objects.all()[:8]
        context['warning_products'] = Product.objects.filter(safe_warning=True)[:10]
        return context
