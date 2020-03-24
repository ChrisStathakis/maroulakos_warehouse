from django.urls import path

from .views import (PaymentInvoiceListView, PaymentInvoiceCreateView, PaymentInvoiceUpdateView, print_invoice_view,
                    PaymentInvoiceCreateFromOrderView, CostumerHomepageView
                    )
from .ajax_views import (ajax_create_item, update_costumer_detail_view, ajax_delete_order_item)

from .views import (CostumerListView, CostumerDetailView, CostumerCreateView,
                    empty_costumer_log_view, CreatePaymentFromCostumerDetailView, EditPaymentFromCostumerView,
                    delete_payment_from_costumer, PrintListView, CostumerHomepageView
                    )
from .ajax_views import (quick_view_costumer_view, quick_pay_costumer_view, ajax_calculate_balance, ajax_analysis_view,
                         ajax_quick_order_view, ajax_quick_payment_view, create_costumer_invoice_view)


app_name = 'costumers'

urlpatterns = [


    path('home/', CostumerHomepageView.as_view(), name='homepage'),
    path('payment-invoice-create/', PaymentInvoiceCreateView.as_view(), name='payment_invoice_create'),
    path('payment-invoice-create-from-costumer/<int:pk>', PaymentInvoiceCreateFromOrderView.as_view(),
         name='payment_invoice_create_costumer'),
    path('payment-update/<int:pk>/', PaymentInvoiceUpdateView.as_view(), name='payment_invoice_update'),

    path('ajax/create/<int:pk>/', ajax_create_item, name='ajax_create_item'),
    path('ajax/delete/<int:pk>/', ajax_delete_order_item, name='ajax_delete_order_item'),
    path('print/<int:pk>/', print_invoice_view, name='print_invoice'),
    path('update-invoice-profile/<int:pk>/', update_costumer_detail_view, name='update_invoice_profile'),



    path('costumers/', CostumerListView.as_view(), name='costumer_list'),
    path('costumer-homepage/', CostumerHomepageView.as_view(), name='costumer_homepage'),
    path('costumers/create/', CostumerCreateView.as_view(), name='costumers_create'),
    path('costumer/detail-view/<int:pk>/', CostumerDetailView.as_view(), name='costumer_detail_view'),

    path('costumer/create/payment/<int:pk>/', CreatePaymentFromCostumerDetailView.as_view(),
         name='create_payment_costumer_detail'),
    path('costumer/detail/<int:pk>/', CostumerDetailView.as_view(), name='costumer_detail'),


    path('costumer/empty/log/<int:pk>/', empty_costumer_log_view, name='costumer_empty_log'),



    path('payment/order/edit/<int:pk>/', EditPaymentFromCostumerView.as_view(), name='edit_payment_from_costumer'),
    path('payment/order/delete/<int:pk>/', delete_payment_from_costumer, name='delete_payment_from_costumer'),




    # ajax
    path('costumer/quick_view/<int:pk>/', quick_view_costumer_view, name='costumer_quick_view'),
    path('costumer/quick-pay/<int:pk>/', quick_pay_costumer_view, name='costumer_quick_pay'),
    path('ajax/costumer-calculate-balance/', ajax_calculate_balance, name='ajax_calculate_balance'),
    path('ajax/analysis/costumers/', ajax_analysis_view, name='ajax_analysis_view'),
    path('ajax/order-quick-view/<int:pk>/', ajax_quick_order_view, name='ajax_quick_order_view'),
    path('ajax/payment-quick-view/<int:pk>/', ajax_quick_payment_view, name='ajax_quick_payment_view'),


    path('print-costumers/', PrintListView.as_view(), name='print_list'),
    path('create-invoice-from-order/<int:pk>/', create_costumer_invoice_view, name='create_costu_inv_from_order')


]
