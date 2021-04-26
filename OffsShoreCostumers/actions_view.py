from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.conf import settings

import datetime
from itertools import chain
from operator import attrgetter

from .models import OffshoreOrder, OffsShoreCompanyCostumer, OffshorePayment
from .forms import OffshoreOrderForm, OffshorePaymentForm

CURRENCY = settings.CURRENCY


@method_decorator(staff_member_required, name='dispatch')
class CreateOrderView(CreateView):
    template_name = 'offshore/form_view.html'
    model = OffshoreOrder
    form_class = OffshoreOrderForm

    def dispatch(self, request, *args, **kwargs):
        self.customer = get_object_or_404(OffsShoreCompanyCostumer, id=self.kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.customer.get_absolute_url()

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['customer'] = self.customer
        return initial

    def get_context_data(self, **kwargs):
        context = super(CreateOrderView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΔΗΜΙΟΥΡΓΙΑ ΠΑΡΑΣΤΑΤΙΚΟΥ ΓΙΑ ΤΟΝ ΠΕΛΑΤΗ {self.customer}'
        context['back_url'] = self.get_success_url()
        return context

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class CreatePaymentView(CreateView):
    template_name = 'offshore/form_view.html'
    form_class = OffshorePaymentForm
    model = OffshorePayment

    def dispatch(self, request, *args, **kwargs):
        self.customer = get_object_or_404(OffsShoreCompanyCostumer, id=self.kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.customer.get_edit_url()

    def get_initial(self):
        initial = super(CreatePaymentView, self).get_initial()
        initial = initial.copy()
        initial['customer'] = self.customer
        return initial

    def get_context_data(self, **kwargs):
        context = super(CreatePaymentView, self).get_context_data(**kwargs)
        context['page_title'] = f'Δηιουργία Πληρωμής για {self.customer}'
        context['back_url'] = self.get_success_url()
        return context

    def form_valid(self, form):
        form.save(form)
        return super(CreatePaymentView, self).form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class OrderUpdateView(UpdateView):
    form_class = OffshoreOrderForm
    template_name = 'offshore/form_view.html'
    model = OffshoreOrder

    def get_success_url(self):
        return self.object.customer.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = f'Επεξεργασια {self.object}'
        context['back_url'] = self.get_success_url()
        context['delete_url'] = ''
        return context

    def form_valid(self, form):
        form.save()
        return super(OrderUpdateView, self).form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class PaymentUpdateView(UpdateView):
    template_name = 'offshore/form_view.html'
    form_class = OffshorePaymentForm
    model = OffshorePayment

    def get_success_url(self):
        return self.object.customer.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PaymentUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = f'Επεξεργασια {self.object}'
        context['back_url'] = self.get_success_url()
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        return super(PaymentUpdateView, self).form_valid(form)


@staff_member_required
def delete_order_view(request, pk):
    obj = get_object_or_404(OffshoreOrder, id=pk)
    obj.delete()
    return redirect(obj.customer.get_edit_url())


@staff_member_required
def delete_payment_view(request, pk):
    obj = get_object_or_404(OffshorePayment, id=pk)
    obj.delete()
    return redirect(obj.customer.get_edit_url())


@staff_member_required
def print_customer_movements_view(request, pk):
    obj = get_object_or_404(OffsShoreCompanyCostumer, id=pk)
    year = request.GET.get('year')
    try:
        year = int(year)
    except:
        return redirect(obj.get_edit_url())

    orders = obj.orders.filter(date__year=year)
    payments = obj.payments.filter(date__year=year)
    merged_qs = sorted(
        chain(orders, payments),
        key=attrgetter('date')
    )
    orders_sum = orders.aggregate(Sum('value'))['value__sum'] if orders.exists() else 0
    payments_sum = payments.aggregate(Sum('value'))['value__sum'] if payments.exists() else 0

    pre_orders = obj.orders.filter(date__lt=datetime.datetime.now().replace(day=1, month=1, year=year))
    pre_payments = obj.payments.filter(date__lt=datetime.datetime.now().replace(day=1, month=1, year=year))
    pre_orders_sum = pre_orders.aggregate(Sum('value'))['value__sum'] if pre_orders.exists() else 0
    pre_payments_sum = pre_payments.aggregate(Sum('value'))['value__sum'] if pre_payments.exists() else 0
    pre_diff = pre_orders_sum - pre_payments_sum
    currency = CURRENCY
    diff = orders_sum + pre_diff - payments_sum
    return render(request, 'offshore/print_view.html', context=locals())