from django.contrib import admin
from .warehouse_models import InvoiceTransformationItem


@admin.register(InvoiceTransformationItem)
class Cderer(admin.ModelAdmin):
    pass