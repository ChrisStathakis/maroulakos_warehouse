from django.urls import path
from .views import (HomepageView,
                    ProductTransformationListView, ProductTransformationPrepareView,
                    VendorListView, CreateVendorView, UpdateVendorView, delete_vendor_view,
                    VendorCardView, VendorNotesView,
                    InvoiceDetailView, InvoiceListView, delete_invoice_view, CreateInvoiceView
                    )
from .action_views import (validate_invoice_form_view, create_product_from_invoice, validate_order_item_creation_view,
                           validate_invoice_edit_view
                           )
from .ajax_views import (ajax_create_product_modal, ajax_modify_order_item_modal, ajax_modify_invoice_view,

                         )


app_name = 'warehouse'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('product-trans/', ProductTransformationListView.as_view(), name='transform_list'),
    path('product-prepare/<int:pk>/', ProductTransformationPrepareView.as_view(), name='transform_prepare'),


    path('vendor-list/', VendorListView.as_view(), name='vendor_list'),
    path('vendor-create/', CreateVendorView.as_view(), name='vendor_create'),
    path('vendor-update/<int:pk>/', UpdateVendorView.as_view(), name='vendor_update'),
    path('vendor-delelte/vendor/<int:pk>/', delete_vendor_view, name='vendor_delete'),
    path('vendor-kartela/<int:pk>/', VendorCardView.as_view(), name='vendor_card'),

    path('invoice-list/', InvoiceListView.as_view(), name='invoice_list'),
    path('invoice-create/', CreateInvoiceView.as_view(), name='invoice_create'),
    path('invoice-detail/<int:pk>/', InvoiceDetailView.as_view(), name='invoice_update'),
    path('invoice-delete-<int:pk>/', delete_invoice_view, name='invoice_delete'),

    # actions
    path('action-invoice-validation/<int:pk>/', validate_invoice_form_view, name='invoice_validation'),
    path('action-create-product-from-invoice/<int:pk>/', create_product_from_invoice, name='create_product_from_invoice'),
    path('validate-order-item-creation/<int:pk>/', validate_order_item_creation_view, name='validate_order_item_creation'),
    path('validate-invoice-edit/<int:pk>/', validate_invoice_edit_view, name='validate_invoice_edit'),

    # ajax 
    path('ajax-create-product-from-invoice/<int:pk>/<int:dk>/', ajax_create_product_modal, name='ajax_create_product'),
    path('ajax-modify-order-item-modal/<int:pk>/', ajax_modify_order_item_modal, name='ajax_modify_order_item'),
    path('ajax-modify-invoice/<int:pk>/', ajax_modify_invoice_view, name='ajax_modify_invoice'),
    
]
