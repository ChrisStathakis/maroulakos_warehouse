from django.urls import path

from .views import (CompanyListView, CompanyCreateView, CompanyUpdateView, company_delete_view,
                    create_costumer_from_company_view, costumer_company_card_view, delete_customer_view
                    )

from .actions_view import (CreateOrderView, OrderUpdateView, delete_order_view,
                           PaymentUpdateView, delete_payment_view,
                           print_customer_movements_view, CreatePaymentView,
                           update_or_delete_company_view)

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
    path('print-movements/<int:pk>/', print_customer_movements_view, name='print_customer_movements'),




    path('actions/order/<int:pk>/', CreateOrderView.as_view(), name='create_order'),
    path('actions/order-update/<int:pk>/', OrderUpdateView.as_view(), name='update_order'),
    path('actions/order-delete/<int:pk>/', delete_order_view, name='delete_order'),

    path('create/payments/<int:pk>/', CreatePaymentView.as_view(), name='create_payment'),
    path('actions/payments-update/<int:pk>/', PaymentUpdateView.as_view(), name='update_payment'),
    path('actions/payments-delete/<int:pk>/', delete_payment_view, name='delete_payment'),

    path('update-or-delete-company/<int:pk>/<slug:action>/', update_or_delete_company_view, name='update_or_delete_company'),
    path('delete-customer/<int:pk>/', delete_customer_view, name='delete_customer'),

    # ajax
    path('costumer/quick_view/<int:pk>/', quick_view_costumer_view, name='costumer_quick_view'),
    path('costumer/quick-pay/<int:pk>/', quick_pay_costumer_view, name='costumer_quick_pay'),
    path('ajax/costumer-calculate-balance/', ajax_calculate_balance, name='ajax_calculate_balance'),
    path('ajax/analysis/costumers/', ajax_analysis_view, name='ajax_analysis_view'),
    path('ajax/order-quick-view/<int:pk>/', ajax_quick_order_view, name='ajax_quick_order_view'),
    path('ajax/payment-quick-view/<int:pk>/', ajax_quick_payment_view, name='ajax_quick_payment_view'),

]