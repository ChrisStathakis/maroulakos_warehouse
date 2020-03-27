from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse, get_object_or_404, redirect

from .models import Vendor, Note, InvoiceItem, Invoice
from .warehouse_models import InvoiceTransformation, InvoiceTransformationItem, InvoiceTransformationIngredient

from .forms import (VendorForm, PaymentForm, InvoiceForm, NoteForm, InvoiceVendorDetailForm,
                    InvoiceProductForm, InvoiceTransformationForm
                    )
from catalogue.models import Product, ProductStorage, Category
from .tables import ProductTransTable, VendorTable, InvoiceTable, InvoiceTransformationTable, VendorProductTable
from .mixins import ListViewMixin

from django_tables2 import RequestConfig

from decimal import Decimal


@method_decorator(staff_member_required, name='dispatch')
class ReportHomepageView(TemplateView):
    template_name = 'warehouse/analysis/homepage.html'


@method_decorator(staff_member_required, name='dispatch')
class InvoiceListAnalysisView(ListView):
    template_name = 'warehouse/analysis/invcoice_list_analysis.html'
    model = Invoice

    def get_queryset(self):
        return self.model.filters_data(self.request, self.model.objects.all())

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'], context['vendor_filter'] = [True] * 2
        context['vendors_analysis'] = self.object_list.values('vendor__title').annotate(total=Sum('final_value'),
                                                                                        count=Count('id')
                                                                                        ).order_by('vendor__title')
        vendor_ids = self.object_list.values_list('vendor__id')
        context['vendors'] = Vendor.objects.filter(id__in=vendor_ids)
        context['month_analysis'] = self.object_list.annotate(month=TruncMonth('date')).values('month').\
            annotate(total=Sum('final_value')).values('month', 'total').order_by('month')
        return context


@method_decorator(staff_member_required, name='dispatch')
class InvoiceItemListAnalysisView(ListView):
    template_name = 'warehouse/analysis/invoice_item_analysis.html'
    model = InvoiceItem

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'], context['vendor_filter'] = [True] * 2
        context['product_analysis'] = self.object_list.values('product__title').annotate(total=Sum('total_value'),
                                                                                         count=Sum('qty')
                                                                                         ).order_by('product__title')
        vendor_ids = self.object_list.values_list('vendor__id')
        context['vendors'] = Vendor.objects.filter(id__in=vendor_ids)
        context['month_analysis'] = self.object_list.annotate(month=TruncMonth('invoice__date')).values('month'). \
            annotate(total=Sum('total_value')).values('month', 'total').order_by('month')
        return context





