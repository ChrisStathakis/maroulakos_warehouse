from django.shortcuts import render, reverse, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, TemplateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from django_tables2 import RequestConfig

from .models import GenericExpense, GenericExpenseCategory, GenericExpensePerson
from .forms import GenericExpenseForm, GenericExpensePersonForm, GenericExpenseCategoryForm
from .tables import GenericExpenseTable, GenericExpensePersonTable, GenericExpenseCategoryTable

from datetime import timedelta
from dateutil.relativedelta import relativedelta


@method_decorator(staff_member_required, name='dispatch')
class GenericExpenseListView(ListView):
    template_name = 'payroll/list.html'
    model = GenericExpense
    paginate_by = 50

    def get_queryset(self):
        return self.model.filters_data(self.request, GenericExpense.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = GenericExpenseTable(self.object_list)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(qs_table)
        context['create_url'] = reverse('payroll_bills:generic_expense_create')
        context['back_url'] = reverse('payroll_bills:home')
        context['queryset_table'] = qs_table
        context['persons'] = GenericExpensePerson.objects.all()
        context['categories'] = GenericExpensePerson.objects.all()
        context['date_filter'], context['search_filter'], context['person_cate_filter'], context['person_filter'] \
            = [True] * 4
        return context


@method_decorator(staff_member_required, name='dispatch')
class GenericExpenseCreateView(CreateView):
    template_name = 'payroll/form.html'
    form_class = GenericExpenseForm
    model = GenericExpense
    success_url = reverse_lazy('payroll_bills:generic_expense_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = 'Δημιουργια Γενικου Εξοδου'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Νεο Γενικο Εξοδο Δημιουργηθηκε')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class GenericExpenseUpdateView(UpdateView):
    template_name = 'payroll/form.html'
    form_class = GenericExpenseForm
    model = GenericExpense
    success_url = reverse_lazy('payroll_bills:generic_expense_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = f'{self.object}'
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η μισθοδοσια επεξεργαστηκε.')
        return super().form_valid(form)


@staff_member_required
def generic_expense_delete_view(request, pk):
    instance = get_object_or_404(GenericExpense, id=pk)
    instance.delete()
    messages.warning(request, 'Το Παραστατικο διαγραφηκε.')
    return redirect(reverse('payroll_bills:generic_expense_list'))


@method_decorator(staff_member_required, name='dispatch')
class GenericExpensePersonListView(ListView):
    template_name = 'payroll/list.html'
    model = GenericExpensePerson
    paginate_by = 50

    def get_queryset(self):
        return self.model.filters_data(self.request, self.model.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = GenericExpensePersonTable(self.object_list)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(qs_table)
        context['create_url'] = reverse('payroll_bills:generic_person_create')
        context['back_url'] = reverse('payroll_bills:home')
        context['queryset_table'] = qs_table
        return context


@method_decorator(staff_member_required, name='dispatch')
class GenericExpensePersonCreateView(CreateView):
    template_name = 'payroll/form.html'
    form_class = GenericExpensePersonForm
    model = GenericExpensePerson
    success_url = reverse_lazy('payroll_bills:generic_person_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = 'Δημιουργια Προσωπου'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Νεο Προσωπο Δημιουργηθηκε')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class GenericExpensePersonUpdateView(UpdateView):
    template_name = 'payroll/form.html'
    form_class = GenericExpensePersonForm
    model = GenericExpensePerson
    success_url = reverse_lazy('payroll_bills:generic_person_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('payroll_bills:generic_person_list')
        context['form_title'] = f'{self.object}'
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η μισθοδοσια επεξεργαστηκε.')
        return super().form_valid(form)


@staff_member_required
def generic_person_delete_view(request, pk):
    instance = get_object_or_404(GenericExpensePerson, id=pk)
    instance.delete()
    messages.warning(request, 'Το Παραστατικο διαγραφηκε.')
    return redirect(reverse('payroll_bills:generic_person_list'))


@method_decorator(staff_member_required, name='dispatch')
class GenericExpenseCategoryListView(ListView):
    template_name = 'payroll/list.html'
    model = GenericExpenseCategory
    paginate_by = 50

    def get_queryset(self):
        return self.model.filters_data(self.request, GenericExpense.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs_table = GenericExpenseCategoryTable(self.object_list)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(qs_table)
        context['create_url'] = reverse('payroll_bills:generic_category_create')
        context['back_url'] = reverse('payroll_bills:home')
        context['queryset_table'] = qs_table

        return context


@method_decorator(staff_member_required, name='dispatch')
class GenericExpenseCategoryCreateView(CreateView):
    template_name = 'payroll/form.html'
    form_class = GenericExpenseCategoryForm
    model = GenericExpenseCategory
    success_url = reverse_lazy('payroll_bills:generic_category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.success_url
        context['form_title'] = 'Δημιουργια Κατηγοριας'
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Νεα κατηγορια Δημιουργηθηκε')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class GenericExpenseCategoryUpdateView(UpdateView):
    template_name = 'payroll/form.html'
    form_class = GenericExpenseCategoryForm
    model = GenericExpenseCategory
    success_url = reverse_lazy('payroll_bills:generic_category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = reverse('payroll_bills:generic_category_list')
        context['form_title'] = f'{self.object}'
        context['delete_url'] = self.object.get_delete_url()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Η Κατηγορια επεξεργαστηκε.')
        return super().form_valid(form)


@staff_member_required
def expense_category_delete_view(request, pk):
    instance = get_object_or_404(GenericExpenseCategory, id=pk)
    instance.delete()
    messages.warning(request, 'Το Παραστατικο διαγραφηκε.')
    return redirect(reverse('payroll_bills:generic_category_list'))
