from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
import datetime

from .models import OffshoreOrder, OffsShoreCompanyCostumer
from .forms import OffshoreOrderForm


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


@staff_member_required
def print_customer_movements_view(request, pk, year):
    obj = get_object_or_404(OffsShoreCompanyCostumer, id=pk)
    orders = obj.orders.filter(date__year=year)
    payments = obj.payments.filter(date__year=year)
    pre_orders = obj.orders.filter(date__lt=datetime.datetime.now().replace(day=1, month=1, year=year))
    pre_payments = obj.payments.filter(date__lt=datetime.datetime.now().replace(day=1, month=1, year=year))
    pre_orders_sum = pre_orders.aggregate(Sum('value'))['value__sum'] if pre_orders.exists() else 0

    return render(request, 'offshore/print_movements.html', context=locals())