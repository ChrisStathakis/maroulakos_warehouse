from django.urls import path

from .views import (CompanyListView, CompanyCreateView, CompanyUpdateView, company_delete_view,
                    create_costumer_from_company_view, costumer_company_card_view
                    )

app_name = 'offshore'

urlpatterns = [
    path('company/list/', CompanyListView.as_view(), name='company_list'),
    path('company/create/', CompanyCreateView.as_view(), name='company_create'),
    path('company/update/<int:pk>/', CompanyUpdateView.as_view(), name='company_update'),
    path('company/delete/<int:pk>/', company_delete_view, name='company_delete'),

    path('create-costumer_from_company_view/<int:pk>/', create_costumer_from_company_view, name='create_company_from_list'),
    path('costumer-company-card/<int:pk>/', costumer_company_card_view, name='costumer_company_card'),

]