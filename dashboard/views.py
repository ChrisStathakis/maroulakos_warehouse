from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.db.models import Sum


@method_decorator(staff_member_required, name='dispatch')
class DashboardHomepageView(TemplateView):
    template_name = 'dashboard.html'