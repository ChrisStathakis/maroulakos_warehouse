from django.urls import path

from .views import (CompanyListView, CompanyCreateView, CompanyUpdateView, company_delete_view,
                    create_costumer_from_company_view, costumer_company_card_view
                    )

from .actions_view import (CreateOrderView, )
from .ajax_views import (quick_view_costumer_view, quick_pay_costumer_view, ajax_calculate_balance,
                         ajax_analysis_view, ajax_quick_order_view, ajax_quick_payment_view)


app_name = 'offshore'

urlpatterns = [
    path('company/list/', CompanyListView.as_view(), name='company_list'),
    path('company/create/', CompanyCreateView.as_view(), name='company_create'),
    path('company/update/<int:pk>/', CompanyUpdateView.as_view(), name='company_update'),
    path('company/delete/<int:pk>/', company_delete_view, name='company_delete'),

    path('create-costumer_from_company_view/<int:pk>/', create_costumer_from_company_view, name='create_company_from_list'),
    path('costumer-company-card/<int:pk>/', costumer_company_card_view, name='costumer_company_card'),




    path('actions/order/<int:pk>/', CreateOrderView.as_view(), name='create_order'),

    # ajax
    path('costumer/quick_view/<int:pk>/', quick_view_costumer_view, name='costumer_quick_view'),
    path('costumer/quick-pay/<int:pk>/', quick_pay_costumer_view, name='costumer_quick_pay'),
    path('ajax/costumer-calculate-balance/', ajax_calculate_balance, name='ajax_calculate_balance'),
    path('ajax/analysis/costumers/', ajax_analysis_view, name='ajax_analysis_view'),
    path('ajax/order-quick-view/<int:pk>/', ajax_quick_order_view, name='ajax_quick_order_view'),
    path('ajax/payment-quick-view/<int:pk>/', ajax_quick_payment_view, name='ajax_quick_payment_view'),

]