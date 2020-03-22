from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


from .models import SalesInvoice, SalesInvoiceItem
from catalogue.models import Product

from .forms import SalesInvoiceItemForm, SalesInvoiceItemForm


@staff_member_required
def ajax_product_modal_view(request, pk, dk):
    instance = get_object_or_404(SalesInvoice, id=pk)
    product = get_object_or_404(Product, id=dk)
    form = SalesInvoiceItemForm(initial={'product': product, 'invoice': instance, 'costumer': instance.costumer})
    success_url = reverse('point_of_sale:validate_order_item_creation', kwargs={'pk': instance.id, 'dk': product.id})
    if product.product_class.have_storage:
        form.fields['storage'].queryset = product.storages.all()
        form.fields['storage'].required = True
    else:
        form.fields['storage'] = forms.HiddenInput()
    data = dict()
    data['modal'] = render_to_string(template_name='point_of_sale/ajax/modal.html',
                                     request=request,
                                     context={'form': form, 'success_url': success_url, 'title': ''}
                                     )
    return JsonResponse(data)


@staff_member_required
def ajax_order_item_edit_modal(request, pk):
    instance = get_object_or_404(SalesInvoiceItem, id=pk)
    form = SalesInvoiceItemForm(instance=instance)
    data = dict()
    data['modal'] = render_to_string(template_name='point_of_sale/ajax/modal.html',
                                     request=request,
                                     context={'form': form,
                                              'title': 'Edit',
                                              'success_url': reverse('point_of_sale:validate_order_item_edit',
                                                                     kwargs={'pk': instance.id})}
                                     )
    return JsonResponse(data)