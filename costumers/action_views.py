from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import  Costumer
from .forms import CostumerPaymentForm


@staff_member_required
def validate_payment_creation(request, pk):
    instance = get_object_or_404(Costumer, id=pk)
    form = CostumerPaymentForm(request.POST or None, initial={'customer': instance})
    if form.is_valid():
        form.save()
        messages.success(request, 'Νεα Πληρωμη Προστεθηκε')
    return redirect(instance.get_edit_url())
