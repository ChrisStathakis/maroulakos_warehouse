from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse

from .models import SalesInvoice, SalesInvoiceItem
from catalogue.models import Product
from .forms import SalesInvoiceItemForm, SaleInvoiceItemForm


@staff_member_required
def validate_order_item_creation(request, pk, dk):
    instance = get_object_or_404(SalesInvoice, id=pk)
    product = get_object_or_404(Product, id=dk)
    form = SalesInvoiceItemForm(request.POST or None, initial={'product': product, 'invoice': instance})
    if form.is_valid():
        form.save()
    else:
        print(form.errors)
    instance.refresh_from_db()
    data = dict()
    data['result'] = render_to_string(template_name='point_of_sale/ajax/order_container.html',
                                      request=request,
                                      context={'object': instance}
                                      )
    return JsonResponse(data)


@staff_member_required
def validate_order_item_edit_view(request, pk):
    instance = get_object_or_404(SalesInvoiceItem, id=pk)
    form = SaleInvoiceItemForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
    invoice = instance.invoice
    invoice.refresh_from_db()
    data = dict()
    data['result'] = render_to_string(template_name='point_of_sale/ajax/order_container.html',
                                      request=request,
                                      context={'object': instance}
                                      )
    return JsonResponse(data)


    
