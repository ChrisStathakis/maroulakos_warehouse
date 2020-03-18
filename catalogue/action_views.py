from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, reverse
from .models import Product, ProductStorage

from .forms import ProductStorageForm, ProductIngredientForm


@staff_member_required
def create_storage_form_view(request, pk):
    instance = get_object_or_404(Product, id=pk)
    form = ProductStorageForm(request.POST or None, initial={'product': instance})
    if form.is_valid():
        form.save()
    else:
        print('errors', form.errors)
    return redirect(instance.get_edit_url())


@staff_member_required
def create_product_ingredient_view(request, pk):
    instance = get_object_or_404(Product, id=pk)
    form = ProductIngredientForm(request.POST or None, initial={'product': instance})
    if form.is_valid():
        form.save()
    else:
        print('errors', form.errors)
    return redirect(instance.get_edit_url())


