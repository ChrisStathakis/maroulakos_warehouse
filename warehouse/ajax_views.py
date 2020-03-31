from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.db.models import Sum
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Invoice, Product, InvoiceItem
from project_settings.models import Storage
from catalogue.models import ProductStorage
from .forms import InvoiceItemForm, InvoiceForm


@staff_member_required
@csrf_exempt
def ajax_modify_order_item_modal(request, pk):
    instance = get_object_or_404(InvoiceItem, id=pk)
    form = InvoiceItemForm(instance=instance)
    data = dict()
    data['result'] = render_to_string(template_name='warehouse/ajax/product_modal.html',
                                      request=request,
                                      context={
                                          'form': form,
                                          'title': f'Επεξεργασια {instance.product}',
                                          'action_url': reverse('warehouse:validate_order_item_update', kwargs={'pk': instance.id}),
                                          'delete_url': instance.get_delete_url()

                                      }
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_create_product_modal(request, pk, dk):
    invoice = get_object_or_404(Invoice, id=pk)
    product = get_object_or_404(Product, id=dk)
    data = dict()
    action_url = reverse("warehouse:validate_order_item_creation", kwargs={'pk': invoice.id})
    form = InvoiceItemForm(initial={
                                    'vendor': invoice.vendor,
                                    'invoice': invoice,
                                    'product': product,
                                    'unit': product.unit,
                                    'taxes_modifier': product.taxes_modifier,
                                    'discount': product.order_discount,
                                    'value': product.price_buy,
                                    'order_code': product.order_sku
                                    }
                           )
    if not product.product_class.have_storage:
        form.fields['storage'].widget = forms.HiddenInput()
    else:
        qs = ProductStorage.objects.filter(product=product)
        if qs.exists():
            form.fields['storage'].queryset = qs
            form.fields['storage'].required = True
        else:
            form.fields['storage'].widget = forms.HiddenInput()
            form.fields['create_storage'] = forms.ModelChoiceField(queryset=Storage.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
            form.fields['create_storage'].required = True
    data['result'] = render_to_string(request=request,
                                      template_name='warehouse/ajax/product_modal.html',
                                      context={
                                          'form': form,
                                          'product': product,
                                          'action_url': action_url,
                                          'invoice': invoice
                                          }
                                    )
    return JsonResponse(data)

