from django.urls import path

from .views import (PointOfSaleHomepageView,
                    SalesListView, SalesCreateView, SalesUpdateView, delete_sales_invoice_view
                    )
from .ajax_views import ajax_product_modal_view, ajax_order_item_edit_modal
from .action_views import validate_order_item_creation, validate_order_item_edit_view
app_name = 'point_of_sale'

urlpatterns = [
    path('', PointOfSaleHomepageView.as_view(), name='homepage'),

    path('sales/list/', SalesListView.as_view(), name='sales_list'),
    path('sales/create/', SalesCreateView.as_view(), name='sales_create'),
    path('sales/update/<int:pk>/', SalesUpdateView.as_view(), name='sales_update'),
    path('sales/delete/<int:pk>/', delete_sales_invoice_view, name='sales_delete'),

    #
    path('ajax/show-product-modal/<int:pk>/<int:dk>', ajax_product_modal_view, name='ajax_product_modal'),
    path('ajax/show-order-item-modal/<int:pk>/', ajax_order_item_edit_modal, name='ajax_order_item_modal'),
    path('validate/order-item-creation/<int:pk>/<int:dk>/', validate_order_item_creation, name='validate_order_item_creation'),
    path('validate/order-item/edit/<int:pk>/', validate_order_item_edit_view, name='validate_order_item_edit')
]
