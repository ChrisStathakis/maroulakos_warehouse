from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


from .models import SalesInvoice, SalesInvoiceItem
from catalogue.models import Product

from .forms import SaleInvoiceItemForm


@staff_member_required
def ajax_search_products(request, pk):
    instance = get_object_or_404(SalesInvoice, id=pk)
    products = Product.filters_data(request, Product.objects.filter(active=True))
    data = dict()
    data['result'] = render_to_string(template_name='point_of_sale/ajax/product_container.html',
                                      request=request,
                                      context={'object': instance,
                                               'products': products
                                               }
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_order_item_edit_modal(request, pk):
    instance = get_object_or_404(SalesInvoiceItem, id=pk)
    form = SaleInvoiceItemForm(instance=instance)
    data = dict()

    data['modal'] = render_to_string(template_name='point_of_sale/ajax/modal.html',
                                     request=request,
                                     context={'form': form,
                                              'title': 'Edit',
                                              'success_url': reverse('point_of_sale:validate_order_item_edit',
                                                                     kwargs={'pk': instance.id})}
                                     )
    return JsonResponse(data)