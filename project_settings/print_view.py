from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.db import models
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.db.models import Sum

from .models import Storage, PaymentMethod
from catalogue.models import ProductStorage
from warehouse.models import InvoiceItem
from warehouse.warehouse_models import InvoiceTransformationItem, InvoiceTransformationIngredient
from point_of_sale.models import SalesInvoiceItem

from operator import attrgetter
from itertools import chain


@staff_member_required
def storage_movements_view(request, pk):
    date_filter, prodduct_filter = [True]*2
    storage = get_object_or_404(Storage, id=pk)
    products = ProductStorage.objects.filter(storage=storage)
    invoices = InvoiceItem.filters_data(request, InvoiceItem.objects.filter(storage__in=products))
    transformations = InvoiceTransformationItem.filters_data(request, InvoiceTransformationItem.objects.filter(storage__in=products))
    transformations_ingrentients = InvoiceTransformationIngredient.filters_data(request, InvoiceTransformationIngredient.objects.filter(storage__in=products))
    sales_invoices = SalesInvoiceItem.filter_data(request, SalesInvoiceItem.objects.filter(storage__in=products))
    movements = sorted(chain(invoices, transformations, transformations_ingrentients,sales_invoices),key=attrgetter('date'))
    context = locals()
    return render(request, 'project_settings/storage_analysis.html', context)


