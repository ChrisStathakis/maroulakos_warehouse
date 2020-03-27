from django.urls import path
from .views import (HomepageView,
                    ProductTransformationListView, ProductTransformationPrepareView,
                    VendorListView, CreateVendorView, UpdateVendorView, delete_vendor_view,
                    VendorCardView, VendorNotesView, NoteUpdateView, delete_note_view,
                    InvoiceDetailView, InvoiceListView, delete_invoice_view, CreateInvoiceView,
                    InvoiceTransformationListView, InvoiceTransformationDetailView, InvoiceTransformationCreateView
                    )
from .action_views import (validate_invoice_form_view, create_product_from_invoice, validate_order_item_update_view,
                           validate_invoice_edit_view, add_product_to_invoice_trans_view, validate_create_invoice_order_item_view,
                           validate_note_creation_view, delete_invoice_item_view
                           )
from .ajax_views import (ajax_create_product_modal, ajax_modify_order_item_modal

                         )
from .analysis_views import ReportHomepageView, InvoiceListAnalysisView, InvoiceItemListAnalysisView


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

    path('invoice-transformation-list/', InvoiceTransformationListView.as_view(), name='invoice_trans_list'),
    path('invoice-transformation/<int:pk>/', InvoiceTransformationDetailView.as_view(), name='invoice_trans_detail'),
    path('invoice-trans-create/', InvoiceTransformationCreateView.as_view(), name='invoice_trans_create'),

    #  notes
    path('notes/<int:pk>/', VendorNotesView.as_view(), name='notes'),
    path('notes/validate-creation/<int:pk>/', validate_note_creation_view, name='note_create'),
    path('notes/update/<int:pk>/', NoteUpdateView.as_view(), name='note_update'),

    path('notes/delete/<int:pk>/', delete_note_view, name='note_delete'),

    # actions
    path('action-invoice-validation/<int:pk>/', validate_invoice_form_view, name='invoice_validation'),
    path('action-create-product-from-invoice/<int:pk>/', create_product_from_invoice, name='create_product_from_invoice'),
    path('validate-order-item-creation/<int:pk>/', validate_order_item_update_view, name='validate_order_item_update'),
    path('validate-invoice-edit/<int:pk>/', validate_invoice_edit_view, name='validate_invoice_edit'),
    path('validate-order-item_creation/<int:pk>/', validate_create_invoice_order_item_view, name='validate_order_item_creation'),
    path('delete-invoice-item/<int:pk>/', delete_invoice_item_view, name='delete_invoice_item'),

    path('add-product-to-trans-invoice/<int:pk>/<int:dk>/', add_product_to_invoice_trans_view, name='add_product_to_trans_invoice'),

    # ajax 
    path('ajax-create-product-from-invoice/<int:pk>/<int:dk>/', ajax_create_product_modal, name='ajax_create_product'),
    path('ajax-modify-order-item-modal/<int:pk>/', ajax_modify_order_item_modal, name='ajax_modify_order_item'),



    # analysis
    path('analysis/homepage/', ReportHomepageView.as_view(), name='analysis_homepage'),
    path('analysis/order-analysis/', InvoiceListAnalysisView.as_view(), name='invoice_analysis'),
    path('analysis/order-item-analysis/', InvoiceItemListAnalysisView.as_view(), name='invoice_items_analysis'),

    
]
