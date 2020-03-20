from django.urls import path

from .views import (PointOfSaleHomepageView,
                    SalesListView, SalesCreateView, SalesUpdateView, delete_sales_invoice_view
                    )

app_name = 'point_of_sale'

urlpatterns = [
    path('', PointOfSaleHomepageView.as_view(), name='homepage'),

    path('sales/list/', SalesListView.as_view(), name='sales_list'),
    path('sales/create/', SalesCreateView.as_view(), name='sales_create'),
    path('sales/update/<int:pk>/', SalesUpdateView.as_view(), name='sales_update'),
    path('sales/delete/<int:pk>/', delete_sales_invoice_view, name='sales_delete'),
]
