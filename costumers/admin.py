from django.contrib import admin

# Register your models here.
from .models import Costumer


@admin.register(Costumer)
class CostumerAdmin(admin.ModelAdmin):
    pass