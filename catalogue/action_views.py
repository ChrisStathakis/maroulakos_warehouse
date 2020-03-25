from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, reverse
from .models import Product, ProductStorage, ProductIngredient

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


@method_decorator(staff_member_required, name='dispatch')
class ProductIngredientUpdateView(UpdateView):
    template_name = 'catalogue/form_view.html'
    form_class = ProductIngredientForm
    model = ProductIngredient

    def get_success_url(self):
        return self.object.product.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.get_success_url()
        context['form_title'] = f'{self.object}'
        context['delete_url'] = self.object.get
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@staff_member_required
def class_copy_product_view(request, pk):
    instance = get_object_or_404(Product, id=pk)
    object = get_object_or_404(Product, id=pk)
    object.id = None
    object.qty = 0
    object.save()
    object.refresh_from_db()
    for ele in instance.category.all():
        object.category.add(ele)
    if object.product_class.have_ingredient:
        for ingre in instance.ingredients.all():
            object.ingredients.add(ingre)
    object.save()
    messages.success(request, 'To Προϊόν Αντιγραφηκε!')
    return redirect(object.get_edit_url())
