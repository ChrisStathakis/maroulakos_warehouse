from django.urls import path

from .views import (PointOfSaleHomepageView, order_itema_analysis_view,
                    SalesListView, SalesCreateView, update_sale_invoice_view, delete_sales_invoice_view
                    )
from .ajax_views import ajax_order_item_edit_modal, ajax_search_products
from .action_views import create_order_item_view, validate_order_item_edit_view, validate_delete_order_item, popup_costumer, connect_to_warehouse_item_view
app_name = 'point_of_sale'

urlpatterns = [
    path('', PointOfSaleHomepageView.as_view(), name='homepage'),

    path('sales/list/', SalesListView.as_view(), name='sales_list'),
    path('sales/create/', SalesCreateView.as_view(), name='sales_create'),
    path('sales/update/<int:pk>/', update_sale_invoice_view, name='sales_update'),
    path('sales/delete/<int:pk>/', delete_sales_invoice_view, name='sales_delete'),

    path('validate/order-item-creation/<int:pk>/<int:dk>/', create_order_item_view, name='create_order_item_view'),
    path('connect-to-warehouse-view/<int:pk>/', connect_to_warehouse_item_view, name='connect_to_warehouse'),

    #
    path('search-products/<int:pk>/', ajax_search_products, name='ajax_search_products'),
    path('ajax/show-order-item-modal/<int:pk>/', ajax_order_item_edit_modal, name='ajax_order_item_modal'),

    path('validate/order-item/edit/<int:pk>/', validate_order_item_edit_view, name='validate_order_item_edit'),
    path('validadte/order-item-delete/<int:pk>/', validate_delete_order_item, name='validate_order_item_delete'),
    path('popup-costumer/', popup_costumer, name='popup_costumer'),

    path('analysis-order-item/', order_itema_analysis_view, name='analysis_order_item'),
]
