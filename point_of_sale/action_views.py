from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from django import forms
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, reverse

from .models import SalesInvoice, SalesInvoiceItem
from warehouse.warehouse_models import InvoiceTransformationItem
from catalogue.models import Product, ProductStorage
from .forms import SaleInvoiceItemForm
from costumers.forms import CostumerForm


@staff_member_required
def create_order_item_view(request, pk, dk):
    instance = get_object_or_404(SalesInvoice, id=pk)
    product = get_object_or_404(Product, id=dk)
    back_url = instance.get_edit_url()
    form_title = f'δημιουργια {product.final_price}'
    form = SaleInvoiceItemForm(request.POST or None,
                               initial={'product': product,
                                        'invoice': instance,
                                        'costumer': instance.costumer,
                                        'value': product.final_price,
                                        'order_code': product.sku
                                        }
                                )
    '''
    if product.product_class.have_storage:
        form.fields['storage'].queryset = product.storages.all()
        form.fields['storage'].required = True
        if product.favorite_storage():
            form.initial['storage'] = product.favorite_storage()
    '''
    if form.is_valid():
        item = form.save()
        product.update_product_from_sale(item)
        return redirect(back_url)
    else:
        messages.warning(request, form.errors)
    return render(request, template_name='point_of_sale/form_view.html', context=locals())


@staff_member_required
def validate_order_item_edit_view(request, pk):
    instance = get_object_or_404(SalesInvoiceItem, id=pk)
    form = SaleInvoiceItemForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
    return redirect(instance.invoice.get_edit_url())


@staff_member_required
def validate_delete_order_item(request, pk):
    instance = get_object_or_404(SalesInvoiceItem, id=pk)
    order = instance.invoice
    instance.delete()
    return redirect(order.get_edit_url())


@staff_member_required
def popup_costumer(request):
    form = CostumerForm(request.POST or None)
    form_title = 'Δημιουργια Πελάτη'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_costumer");</script>' % (instance.pk, instance))
    return render(request, "point_of_sale/form_view.html", {"form": form, 'form_title': form_title})


@staff_member_required
def connect_to_warehouse_item_view(request, pk):
    sale_item = get_object_or_404(SalesInvoiceItem, id=pk)
    product = sale_item.product
    have_ = product.product_class.have_ingredient
    items = product.storages.all()
    if have_:
        items = InvoiceTransformationItem.objects.filter(product=product)
    return render(request, 'point_of_sale/connect_to_warehouse.html', context=locals())


@staff_member_required
def validate_connect_to_warehouse_view(request, pk, dk):
    sale_item = get_object_or_404(SalesInvoiceItem, id=pk)
    product = sale_item.product
    have_ingre = product.product_class.have_ingredient
    if have_ingre:
        warehouse_item = get_object_or_404(InvoiceTransformationItem, id=dk)
        old_warehouse_item = sale_item.warehouse_item
        old_storage = sale_item.storage
        sale_item.warehouse_item = warehouse_item
        sale_item.storage = warehouse_item.storage
        sale_item.save()

        old_warehouse_item.save() if old_warehouse_item is not None else ''
        old_storage.save() if old_storage is not None else ''
    else:
        old_storage = sale_item.storage
        storage = get_object_or_404(ProductStorage, id=dk)
        sale_item.storage = storage
        sale_item.save()
        old_storage.save() if old_storage is not None else ''
    return redirect(sale_item.invoice.get_edit_url())


@staff_member_required
def print_sale_order_tree_view(request,pk):
    instance = get_object_or_404(SalesInvoice, id=pk)
    return render(request, 'point_of_sale/print/sale_order_tree.html', context=locals())