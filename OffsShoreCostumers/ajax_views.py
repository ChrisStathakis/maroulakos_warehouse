from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.utils import timezone
from django.db.models import Sum

from .models import OffsShoreCompanyCostumer, OffshorePayment, OffshoreOrder


@staff_member_required
def ajax_calculate_balance(request):
    customers = OffsShoreCompanyCostumer.objects.all()
    total_balance = customers.aggregate(Sum('balance'))['balance__sum'] if customers else 0
    data = dict()
    data['result'] = render_to_string(request=request,
                                      template_name='offshore/ajax_views/calculate_balance_view.html',
                                      context={
                                          'total_balance': total_balance
                                      }
                                      )
    return JsonResponse(data)


@staff_member_required
def quick_view_costumer_view(request, pk):
    costumer = get_object_or_404(OffsShoreCompanyCostumer, id=pk)
    data = dict()
    data['result'] = render_to_string(template_name='offshore/ajax_views/quick_view_modal.html',
                                      request=request,
                                      context={
                                          'costumer': costumer
                                      })
    return JsonResponse(data)


@staff_member_required
def quick_pay_costumer_view(request, pk):
    customer = get_object_or_404(OffsShoreCompanyCostumer, id=pk)
    if customer.balance <= 0:
        return redirect(reverse('costumer_list'))
    payment = OffshorePayment.objects.create(customer=customer,
                                     value=customer.balance,
                                     date=timezone.now()
                                     )
    return redirect(reverse('costumer_list'))


@staff_member_required()
def ajax_analysis_view(request):
    date_range = request.GET.get('date_range')
    orders = OffshoreOrder.filters_data(request, OffshoreOrder.objects.all())
    payments = OffshorePayment.filters_data(request, OffshorePayment.objects.all())
    costumers_orders = orders.values('customer__first_name', 'customer__last_name').annotate(
        total=Sum('value')).order_by('-total')
    costumers_payments = payments.values('customer__first_name', 'customer__last_name').annotate(
        total=Sum('value')).order_by('-total')
    total_value = orders.aggregate(Sum('value'))['value__sum'] if orders else 0
    total_payment = payments.aggregate(Sum('value'))['value__sum'] if payments else 0
    difference = total_value - total_payment
    data = dict()
    data['result'] = render_to_string(template_name='offshore/ajax_views/ajax_analysis_view.html',
                                      request=request,
                                      context=locals()
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_quick_order_view(request, pk):
    instance = get_object_or_404(OffshoreOrder, id=pk)
    data = dict()
    data['result'] = render_to_string(template_name='offshore/ajax_views/quick_order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance
                                      }
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_quick_payment_view(request, pk):
    instance = get_object_or_404(OffshorePayment, id=pk)
    data = dict()
    data['result'] = render_to_string(template_name='offshore/ajax_views/quick_order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance
                                      }
                                      )
    return JsonResponse(data)
