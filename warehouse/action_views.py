from django.shortcuts import render, reverse, get_object_or_404, HttpResponseRedirect, redirect
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import InvoiceVendorDetailForm, InvoiceProductForm
from .models import Vendor, Invoice, InvoiceItem



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
    invoice = get_object_or_404(Invoice, id=pk)
    form = InvoiceProductForm(request.POST or None, initial={'vendor': instance.vendor})
    if form.is_valid():
        qty = form.cleaned_data.get('qty', 1)
        product = form.save()
        InvoiceItem.object.create(
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
        return redirect(invoice.get_edit_url())
    else:
        messages.warning(request, form.errors)
    return redirect(invoice.get_edit_url())
    