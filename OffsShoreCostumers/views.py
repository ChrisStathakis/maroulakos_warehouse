from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


from .models import OffsShoreCompany, OffsShoreCostumer, OffsShoreCompanyCostumer
from .forms import (OffshoreCompanyForm, OffshoreCostumerForm)
from .tables import (OffsShoreCompanyTable, OffshoreCompanyCostumerTable, OrderTable, PaymentTable)




@method_decorator(staff_member_required, name='dispatch')
class CompanyListView(ListView):
    template_name = 'offshore/list_view.html'
    model = OffsShoreCompany
    queryset = OffsShoreCompany.objects.all()

    def get_context_data(self, *args,  **kwargs):
        context = super(CompanyListView, self).get_context_data(*args, **kwargs)
        context['create_url'] = reverse('offshore:company_create')
        context['page_title'] = 'ΕΤΑΙΡΙΕΣ'
        context['queryset_table'] = OffsShoreCompanyTable(self.object_list)
        return context


@method_decorator(staff_member_required, name='dispatch')
class CompanyCreateView(CreateView):
    template_name = 'offshore/form_view.html'
    form_class = OffshoreCompanyForm
    success_url = reverse_lazy('offshore:company_list')

    def get_context_data(self, **kwargs):
        context = super(CompanyCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'ΔΗΜΙΟΥΡΓΙΑ ΕΤΑΙΡΙΑΣ'
        context['back_url'] = self.success_url

        return context

    def form_valid(self, form):
        form.save()
        return super(CompanyCreateView, self).form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class CompanyUpdateView(ListView):
    template_name = 'offshore/list_view.html'
    model = OffsShoreCompanyCostumer

    def get_queryset(self):
        self.company = get_object_or_404(OffsShoreCompany, id=self.kwargs['pk'])
        costumers = self.company.offsshorecompanycostumer_set.all()
        return costumers

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = f'ΠΕΛΑΤΕΣ {self.company}'
        context['back_url'] = reverse('offshore:company_list')
        context['create_url'] = reverse('offshore:create_company_from_list', kwargs={'pk': self.company.id})
        qs_table = OffshoreCompanyCostumerTable(self.object_list)

        context['queryset_table'] = qs_table
        return context


@staff_member_required
def company_delete_view(request, pk):
    obj = get_object_or_404(OffsShoreCompany, id=pk)
    obj.delete()
    messages.warning(request, f'Η Εταιρία {obj} διαγράφηκε!')
    return redirect(reverse(''))


# ----------------------------------------costumers------------------------------------------------------------------ #


@staff_member_required
def create_costumer_from_company_view(request, pk):
    company = get_object_or_404(OffsShoreCompany, id=pk)
    form = OffshoreCostumerForm(request.POST or None)
    if form.is_valid():
        costumer = form.save()
        instance = OffsShoreCompanyCostumer.objects.create(
            company=company,
            costumer=costumer
        )
        return redirect(instance.get_absolute_url)
    context = dict()
    context['page_title'] = f'ΔΗΜΙΟΥΡΓΙΑ ΠΕΛΑΤΗ ==> {company}'
    context['back_url'] = company.get_absolute_url()
    context['form'] = form
    return render(request, 'offshore/form_view.html', context)


@staff_member_required
def costumer_company_card_view(request, pk):
    instance = get_object_or_404(OffsShoreCompanyCostumer, id=pk)
    context = locals()
    orders = instance.orders.all()
    payments = instance.payments.all()
    orders_table = OrderTable(orders)
    payments_table = PaymentTable(payments)

    context['date_filter'] = True
    context['orders_table'] = orders_table
    context['payments_table'] = payments_table

    return render(request, 'offshore/costumer_card_view.html', context)


