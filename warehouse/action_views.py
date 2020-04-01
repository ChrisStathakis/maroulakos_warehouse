from django.shortcuts import render, reverse, get_object_or_404, HttpResponseRedirect, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from django.contrib import messages

from .forms import (InvoiceVendorDetailForm, InvoiceProductForm, InvoiceItemForm, InvoiceForm,
                    InvoiceTransformationItemForm, NoteForm, PaymentForm, VendorForm, EmployerForm, VendorBankingAccountForm)
from .models import Vendor, Invoice, InvoiceItem, Product, ProductStorage, VendorBankingAccount, Employer
from .warehouse_models import InvoiceTransformation, InvoiceTransformationIngredient, InvoiceTransformationItem
from project_settings.constants import CURRENCY
from project_settings.models import Storage


@staff_member_required
def validate_payment_form_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = PaymentForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        new_instance = form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_invoice_item_view(request, pk):
    instance = get_object_or_404(InvoiceItem, id=pk)
    instance.delete()
    return redirect(instance.invoice.get_edit_url())


@staff_member_required
def validate_invoice_form_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = InvoiceVendorDetailForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        new_instance = form.save()
        messages.success(request, f'Το παραστατικό {new_instance.title} δημιουργηθηκε.')
        return redirect(new_instance.get_edit_url())
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def create_product_from_invoice(request, pk):
    instance = get_object_or_404(Invoice, id=pk)
    form = InvoiceProductForm(request.POST or None, initial={'vendor': instance.vendor})
    if form.is_valid():
        product = form.save()
        qty = form.cleaned_data.get('qty', 1)
        '''
        new_item =InvoiceItem.object.create(
                    order_code=product.order_sku,
                    vendor=product.vendor,
                    invoice=invoice,    
                    product=product,
                    unit=product.unit,
                    qty=qty,
                    value=product.price_buy,
                    discount=product.order_discount,
                    taxes_modifier=product.taxes_modifier    
                )
        '''
        
        return redirect(instance.get_edit_url())
    else:
        messages.warning(request, form.errors)
    return redirect(instance.get_edit_url())


@staff_member_required
def validate_create_invoice_order_item_view(request, pk):
    instance = get_object_or_404(Invoice, id=pk)
    form = InvoiceItemForm(request.POST or None, initial={'invoice': instance,
                                                          'vendor': instance.vendor,
                                                          })
    form.fields['create_storage'] = forms.ModelChoiceField(queryset=Storage.objects.all(),
                                                           widget=forms.Select(attrs={'class': 'form-control'}),
                                                           required=False)
    if form.is_valid():
        data = form.save()
        product = data.product
        product.price_buy = data.value
        product.order_sku = data.order_code
        product.order_discount = data.discount
        product.save()
        create_storage = form.cleaned_data.get('create_storage', None)
        if create_storage:
            new_storage = ProductStorage.objects.create(
                product=product,
                storage=create_storage,
            )
            data.storage = new_storage
            data.save()
    else:
        print(form.errors)
    return redirect(instance.get_edit_url())


@staff_member_required
def validate_order_item_update_view(request, pk):
    instance = get_object_or_404(InvoiceItem, id=pk)
    form = InvoiceItemForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
    return redirect(instance.invoice.get_edit_url())


@staff_member_required
def validate_invoice_edit_view(request, pk):
    instance = get_object_or_404(Invoice, id=pk)
    form = InvoiceForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, 'Οι αλλαγες Αποθηκευτηκαν')
    return instance.get_edit_url()


@staff_member_required
def add_product_to_invoice_trans_view(request, pk, dk):
    instance = get_object_or_404(InvoiceTransformation, id=pk)
    product_ = get_object_or_404(Product, id=dk)
    form_title, currency = f'Δημιουργια {product_}', CURRENCY
    info_trans = True
    back_url = instance.get_edit_url()
    form = InvoiceTransformationItemForm(request.POST or None, initial={'product': product_,
                                                                        'invoice': instance,
                                                                        'value': product_.final_price
                                                                        })
    form.fields['storage'].queryset = product_.storages.all()
    maximum_uses = None
    for ele in product_.ingredients.all():
        new_qty = ele.ingredient.qty/ele.qty if ele.qty > 0 else 0
        if not maximum_uses:
            maximum_uses = new_qty
        else:
            if new_qty < maximum_uses:
                maximum_uses = new_qty

    if form.is_valid():
        for ele in product_.ingredients.all():
            pr = ele.ingredient
            if pr.product_class.have_storage:
                if not pr.favorite_storage():
                    messages.warning(request, f'{pr.title} δε έχει βασική αποθηκη')
                    return redirect(instance.get_edit_url())
        item = form.save()
        ingredients = product_.ingredients.all()
        qty = item.qty
        for ingre in ingredients:
            pro = ingre.ingredient
            product_qty = qty*ingre.qty
            new_ingre = InvoiceTransformationIngredient.objects.create(
                invoice_item=item,
                product=pro,
                qty=product_qty,
                cost=ingre.cost,
                qty_ratio=ingre.qty

            )
            if pro.favorite_storage():
                new_ingre.storage = pro.favorite_storage()
                new_ingre.save()
        return redirect(instance.get_edit_url())
    return render(request, 'warehouse/form_view.html', context=locals())


@staff_member_required
def validate_note_creation_view(request, pk):
    instance = get_object_or_404(Vendor, id=pk)
    form = NoteForm(request.POST or None, initial={'vendor_related': instance})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_employer_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = EmployerForm(request.POST or None, initial={'vendor': vendor})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@staff_member_required
def delete_transformation_item_view(request, pk):
    instance = get_object_or_404(InvoiceTransformationItem, id=pk)
    instance.delete()
    return redirect(instance.invoice.get_edit_url())


@staff_member_required
def validate_employer_edit_view(request, pk):
    employer = get_object_or_404(Employer, id=pk)
    form = EmployerForm(request.POST or None, instance=employer)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_employer_view(request, pk):
    employer = get_object_or_404(Employer, id=pk)
    employer.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_create_banking_account_view(request, pk):
    vendor = get_object_or_404(Vendor, id=pk)
    form = VendorBankingAccountForm(request.POST, initial={'vendor': vendor})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def validate_edit_banking_account_view(request, pk):
    banking_account = get_object_or_404(VendorBankingAccount, id=pk)
    form = VendorBankingAccountForm(request.POST or None, instance=banking_account)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def delete_banking_account_view(request, pk):
    banking_account = get_object_or_404(VendorBankingAccount, id=pk)
    banking_account.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required
def change_product_favorite_warehouse_view(request):
    new_id = request.POST.get('new_id', None)
    if new_id:
        product_storage = get_object_or_404(ProductStorage, id=new_id)
        product_storage.priority = True
        product_storage.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def popup_vendor(request):
    form = VendorForm(request.POST or None)
    form_title = 'Δημιουργια Προμηθευτη'
    if form.is_valid():
        print('for')
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_vendor");</script>' % (instance.pk, instance))
    return render(request, 'warehouse/form_view.html', context=locals())


