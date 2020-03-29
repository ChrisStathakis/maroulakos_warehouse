from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.db.models import ProtectedError
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, reverse
from .models import Product, ProductStorage, ProductIngredient
from warehouse.forms import VendorForm
from .forms import ProductStorageForm, ProductIngredientForm, CategoryForm
from project_settings.forms import StorageForm


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
        data = form.save()
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


@method_decorator(staff_member_required, name='dispatch')
class ProductStorageUpdateView(UpdateView):
    template_name = 'catalogue/form_view.html'
    model = ProductStorage
    form_class = ProductStorageForm

    def get_success_url(self):
        return self.object.product.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Επεξεργασια {self.object.storage}'
        context['back_url'] = self.get_success_url()
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@staff_member_required
def delete_product_storage_view(request, pk):
    instance = get_object_or_404(ProductStorage, id=pk)
    try:
        instance.delete()
    except ProtectedError:
        messages.warning(request, 'Η αποθηκη χρησιμοποιειτε')
    return redirect(instance.product.get_edit_url())


@method_decorator(staff_member_required, name='dispatch')
class ProductIngredientUpdateView(UpdateView):
    template_name = 'catalogue/form_view.html'
    model = ProductIngredient
    form_class = ProductIngredientForm

    def get_success_url(self):
        return self.object.product.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Επεξεργασια {self.object.product}'
        context['back_url'] = self.get_success_url()
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Το Συστατικο επεξεργαστικε')
        return super().form_valid(form)


@staff_member_required
def ingredient_delete_view(request, pk):
    instance = get_object_or_404(ProductIngredient, id=pk)
    instance.delete()
    return redirect(instance.product.get_edit_url())


@staff_member_required
def popup_vendor(request):
    form = VendorForm(request.POST or None)
    form_title = 'Δημιουργία Προμηθευτή'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_vendor");</script>' % (instance.pk, instance))
    return render(request, "catalogue/form_view.html", locals())


@staff_member_required
def popup_storage(request):
    form = StorageForm(request.POST or None)
    form_title = 'Δημιουργια Αποθηκης'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_storage");</script>' % (instance.pk, instance))
    return render(request, "catalogue/form_view.html", locals())


@staff_member_required
def popup_category(request):
    form = CategoryForm(request.POST or None)
    form_title = 'Δημιουργία Κατηγορίας'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))
    return render(request, "catalogue/form_view.html", {"form": form, 'form_title': form_title})

'''
@staff_member_required
def popup_category(request):
    form = WarehouseCategoryForm(request.POST or None)
    form_title = 'Δημιουργία Κατηγορίας'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))
    return render(request, "dashboard/form.html", {"form": form, 'form_title': form_title})


@staff_member_required
def popup_brand(request):
    form = BrandForm(request.POST or None)
    form_title = 'Δημιουργία Brand'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_brand");</script>' % (instance.pk, instance))
    return render(request, "dashboard/form.html", locals())





@staff_member_required
def popup_color(request):
    form = ColorForm(request.POST or None)
    form_title = 'Δημιουργία Χρώματος'
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#id_color");</script>' % (instance.pk, instance))
    return render(request, "dashboard/form.html", locals())
'''