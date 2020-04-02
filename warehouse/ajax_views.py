from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.db.models import Sum
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_exempt

from .warehouse_models import InvoiceTransformation
from .models import Invoice, Product, InvoiceItem
from project_settings.models import Storage
from catalogue.models import ProductStorage
from .forms import InvoiceItemForm, InvoiceForm, EmployerForm, VendorBankingAccountForm
from .models import Employer, VendorBankingAccount, Vendor


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
def ajax_search_products_view(request, pk):
    instance = get_object_or_404(InvoiceTransformation, id=pk)
    products = Product.filters_data(request, Product.objects.filter(product_class__have_ingredient=True))[:10]
    data = dict()
    data['result'] = render_to_string(template_name='warehouse/ajax/product_container.html',
                                      request=request,
                                      context={
                                          'object': instance,
                                          'products': products
                                      })
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
            form.fields['create_storage'] = forms.ModelChoiceField(queryset=Storage.objects.all(),
                                                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                                                   label='Δημιουργια Αποθηκης'
                                                                   )
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


@staff_member_required
def ajax_employer_edit_modal_view(request, pk):
    employer = get_object_or_404(Employer, id=pk)
    form = EmployerForm(instance=employer)
    form_title, valid_url = f'Επεξεργασία {employer.title}', reverse('warehouse:validate_employer_edit_view',
                                                                     kwargs={'pk': employer.id}
                                                                     )
    delete_url = reverse('warehouse:action_delete_employer', kwargs={'pk': employer.id})
    data = dict()
    data['result'] = render_to_string(request=request,
                                      template_name='warehouse/ajax/modal_form.html',
                                      context=locals(),
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_banking_account_edit_modal_view(request, pk):
    banking_account = get_object_or_404(VendorBankingAccount, id=pk)
    form = EmployerForm(instance=banking_account)
    form_title, valid_url = f'Επεξεργασία {banking_account}', reverse('warehouse:validate_employer_edit_view', kwargs={'pk': banking_account.id})
    delete_url = reverse('warehouse:delete_account_banking_view', kwargs={'pk': banking_account.id})
    data = dict()
    data['result'] = render_to_string(request=request,
                                      template_name='warehouse/ajax/modal_form.html',
                                      context=locals(),
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_banking_account_create_modal_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = VendorBankingAccountForm(initial={'vendor': vendor})
    form_title, valid_url = f'Δημιουργία', reverse('warehouse:validate_create_banking_account', kwargs={'pk': vendor.id})
    data = dict()
    data['result'] = render_to_string(request=request,
                                      template_name='warehouse/ajax/modal_form.html',
                                      context=locals(),
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_banking_account_edit_modal_view(request, pk):
    banking_account = get_object_or_404(VendorBankingAccount, id=pk)
    form = VendorBankingAccountForm(instance=banking_account)
    form_title, valid_url = f'Επεξεργασια', reverse('warehouse:validate_edit_banking_account', kwargs={'pk': banking_account.id})
    delete_url = reverse('warehouse:delete_account_banking_view', kwargs={'pk': banking_account.id})
    data = dict()
    data['result'] = render_to_string(request=request,
                                      template_name='warehouse/ajax/modal_form.html',
                                      context=locals(),
                                      )
    return JsonResponse(data)



