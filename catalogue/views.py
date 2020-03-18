from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.db.models import Sum

from .models import ProductClass, Product, Category
from .tables import ProductClassTable, ProductTable, CategoryTable
from .forms import ProductForm, ProductCreateForm, ProductStorageForm, ProductIngredientForm, ProductClassForm, CategoryForm
from .mixins import ListViewMixin

from django_tables2 import RequestConfig


@method_decorator(staff_member_required, name='dispatch')
class HomepageView(TemplateView):
    template_name = 'catalogue/dashboard.html'


@method_decorator(staff_member_required, name='dispatch')
class ProductClassListView(ListViewMixin, ListView):
    model = ProductClass

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = ProductClassTable(self.object_list)
        RequestConfig(self.request, {'per_page': self.paginate_by}).configure(qs_table)
        context['queryset_table'] = qs_table
        context['create_url'] = reverse('catalogue:product_class_create')
        return context


@method_decorator(staff_member_required, name='dispatch')
class ProductClassCreateView(CreateView):
    model = ProductClass
    template_name = 'catalogue/form_view.html'
    form_class = ProductClassForm
    success_url = reverse_lazy('catalogue:product_class_list_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class ProductListView(ListViewMixin, ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset_table = ProductTable(self.object_list)
        RequestConfig(self.request).configure(queryset_table)
        context['queryset_table'] = queryset_table
        context['create_url'] = reverse('catalogue:product_create')
        return context


@method_decorator(staff_member_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'catalogue/form_view.html'

    def get_success_url(self):
        return self.new_product.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = 'Δημιουργια Προϊόντος'
        context["back_url"] = reverse('catalogue:product_list')
        return context

    def form_valid(self, form):
        self.new_product = form.save()
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalogue/product_update.html'

    def get_success_url(self):
        return self.object.get_edit_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f'{self.object}'
        context['product_storage_form'] = ProductStorageForm(initial={'product': self.object})
        context['product_ingredient_form'] = ProductIngredientForm(initial={'product': self.object})
        context['back_url'] = reverse('catalogue:product_list')
        context['action_url'] = reverse('catalogue:product_list')

        return context


@staff_member_required
def delete_product_view(request, pk):
    instance = get_object_or_404(Product, id=pk)
    instance.delete()
    messages.success(request, f'Το Προϊον {instance.title} διαγραφηκε')
    return redirect(reverse('edit_product_list'))


@staff_member_required
def copy_product_view(request, pk):
    instance = get_object_or_404(Product, id=pk)
    instance.pk = None
    instance.save()
    messages.success(request, 'Το Προιόν αντιγραφηκε επιτυχώς.')
    return redirect(instance.get_edit_url())


@method_decorator(staff_member_required, name='dispatch')
class CategoryListView(ListViewMixin, ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse('catalogue:category_create')
        context['back_url'] = reverse('catalogue:homepage')
        qs_table = CategoryTable(self.object_list)
        context['queryset_table'] =  RequestConfig(self.request, {'per_page': self.paginate_by}).configure(qs_table)
        return context


@method_decorator(staff_member_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalogue/form_view.html'
    success_url = reverse_lazy('catalogue:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = 'Δημιουργια κατηγοριας'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η Κατηγορια Αποθηκευτηκε.')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalogue/form_view.html'
    success_url = reverse_lazy('catalogue:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['delete_url'] = self.object.get_delete_url()
        context['form_title'] = 'Επεξεργασια κατηγοριας'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η Κατηγορια Επεξεργαστηκε.')
        return super().form_valid(form)


@staff_member_required
def category_delete_view(request, pk):
    instance = get_object_or_404(Category, id=pk)
    instance.delete()
    return redirect(reverse('catalogue:category_list'))
