from django.urls import path
from .views import (HomepageView,
                    StorageListView, StorageCreateView, StorageUpdateView, delete_storage_view,
                    PaymentMethodListView, PaymentMethodCreateView, PaymentMethodUpdateView, delete_payment_view,

                    )
from .print_view import storage_movements_view

app_name = 'settings'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('storage-list/', StorageListView.as_view(), name='storage_list'),
    path('storage-create/', StorageCreateView.as_view(), name='storage_create'),
    path('storage-update/<int:pk>/', StorageUpdateView.as_view(), name='storage_update'),
    path('storage-delete/<int:pk>/', delete_storage_view, name='storage_delete'),

    path('payment-list/', PaymentMethodListView.as_view(), name='payment_list'),
    path('payment-create/', PaymentMethodCreateView.as_view(), name='payment_create'),
    path('payment-update/<int:pk>/', PaymentMethodUpdateView.as_view(), name='payment_update'),
    path('payment-delete/<int:pk>/', delete_payment_view, name='payment_delete'),

    path('storage-analysis/<int:pk>/', storage_movements_view, name='storage_analysis')

]
