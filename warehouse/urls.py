from django.urls import path
from .views import (HomepageView,
                    ProductTransformationListView, ProductTransformationPrepareView,
                    VendorListView, CreateVendorView, UpdateVendorView, delete_vendor_view,
                    VendorCardView, VendorNotesView, NoteUpdateView, delete_note_view,
                    InvoiceDetailView, InvoiceListView, delete_invoice_view, CreateInvoiceView,
                    InvoiceTransformationListView, InvoiceTransformationDetailView, InvoiceTransformationCreateView,
                    InvoiceItemTransformationUpdateView, create_sale_invoice_transformation_view
                    )
from .action_views import (validate_invoice_form_view, create_product_from_invoice, validate_order_item_update_view,
                           validate_invoice_edit_view, add_product_to_invoice_trans_view, validate_create_invoice_order_item_view,
                           validate_note_creation_view, delete_invoice_item_view, delete_transformation_item_view, validate_payment_form_view,
                           change_product_favorite_warehouse_view, popup_vendor, print_invoice_transformation,
                           delete_employer_view, validate_employer_edit_view, validate_employer_view, validate_ingredient_order_item_view,
                           delete_banking_account_view, validate_create_banking_account_view, validate_edit_banking_account_view
                           )
from .ajax_views import (ajax_create_product_modal, ajax_modify_order_item_modal,
                         ajax_banking_account_create_modal_view, ajax_banking_account_edit_modal_view, ajax_employer_edit_modal_view,
                         ajax_search_products_view, ajax_edit_ingredient_view
                         )

from .warehouse_movements_view import (WarehouseMovementsInvoiceListView, CreateWarehouseMovementsInvoiceView,
                                       WarehouseMovementsInvoiceUpdateView, delete_warehouse_movements_invoice_view,
                                       validate_add_products_view, delete_ware_move_item)

from .autocomplete import VendorAutocomplete
from .analysis_views import ReportHomepageView, InvoiceListAnalysisView, InvoiceItemListAnalysisView
from .payment_view import PaymentListView, PaymentCreateView, PaymentUpdateView, payment_delete_view
from .invoice_views import InvoiceItemListView

app_name = 'warehouse'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('product-trans/', ProductTransformationListView.as_view(), name='transform_list'),
    path('product-prepare/<int:pk>/', ProductTransformationPrepareView.as_view(), name='transform_prepare'),
    path('create/copy-trans-to-sale/<int:pk>/', create_sale_invoice_transformation_view, name='create_sale_from_trans'),

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
    path('invoice-trans-item-update/<int:pk>/', InvoiceItemTransformationUpdateView.as_view(), name='invoice_item_trans_update'),

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
    path('valdiate/ingre-order-item/<int:pk>/<int:dk>/', validate_ingredient_order_item_view, name='validate_ingre_order_item'),
    path('delete-invoice-item/<int:pk>/', delete_invoice_item_view, name='delete_invoice_item'),
    path('delete-transformation-item/<int:pk>/', delete_transformation_item_view, name='delete_transformation_item'),
    path('aciton-validate-payment-creation/<int:pk>/', validate_payment_form_view, name='validate_payment'),
    path('action-print/<int:pk>/', print_invoice_transformation, name='print_invoice_transformation'),

    path('add-product-to-trans-invoice/<int:pk>/<int:dk>/', add_product_to_invoice_trans_view, name='add_product_to_trans_invoice'),
    path('action/change-favorite-product-storage/', change_product_favorite_warehouse_view, name='quick_favorite_storage'),
    path('popup/create-vendor/', popup_vendor, name='popup_vendor'),

    # ajax 
    path('ajax-create-product-from-invoice/<int:pk>/<int:dk>/', ajax_create_product_modal, name='ajax_create_product'),
    path('ajax-modify-order-item-modal/<int:pk>/', ajax_modify_order_item_modal, name='ajax_modify_order_item'),
    path('ajax/search-products/<int:pk>/', ajax_search_products_view, name='ajax_search_products'),
    path('ajax-edit-ingre-modal/<int:pk>/', ajax_edit_ingredient_view, name='ajax_edit_ingre_modal'),



    # analysis
    path('analysis/homepage/', ReportHomepageView.as_view(), name='analysis_homepage'),
    path('analysis/order-analysis/', InvoiceListAnalysisView.as_view(), name='invoice_analysis'),
    path('analysis/order-item-analysis/', InvoiceItemListAnalysisView.as_view(), name='invoice_items_analysis'),

    #  employer links
    path('actions/validate-employer-edit-form/<int:pk>/', validate_employer_edit_view, name='validate_employer_edit_view'),
    path('actions/employer-delete/<int:pk>/', delete_employer_view, name='action_delete_employer'),
    path('ajax/validate/<int:pk>/', validate_employer_view, name='validate_employer_create'),
    path('ajax/employer-edit/<int:pk>/', ajax_employer_edit_modal_view, name='ajax_edit_employer'),


    # banking accounts
    path('validate/banking-account-create/<int:pk>/', validate_create_banking_account_view,
         name='validate_create_banking_account'),
    path('validate/banking_account-edit/<int:pk>/', validate_edit_banking_account_view,
         name='validate_edit_banking_account'),
    path('banking-account-delete/<int:pk>/', delete_banking_account_view, name='delete_account_banking_view'),


    path('ajax/modal/banking-account/<int:pk>/', ajax_banking_account_create_modal_view,
         name='ajax_create_banking_account'),
    path('ajax/modal/banking-account-edit/<int:pk>/', ajax_banking_account_edit_modal_view,
         name='ajax_edit_banking_account'),
    path('validate/banking-account-create/<int:pk>/', validate_create_banking_account_view,
         name='validate_create_banking_account'),
    path('validate/banking_account-edit/<int:pk>/', validate_edit_banking_account_view,
         name='validate_edit_banking_account'),
    path('banking-account-delete/<int:pk>/', delete_banking_account_view, name='delete_account_banking_view'),

    # payments
    path('payment/list/', PaymentListView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
    path('payment_update/<int:pk>/', PaymentUpdateView.as_view(), name='payment_update'),
    path('payment-delete/<int:pk>/', payment_delete_view, name='payment_delete'),

    # warehouse movements
    path('warehouse-movements-list/', WarehouseMovementsInvoiceListView.as_view(), name='ware_move_list'),
    path('warehouse-movements-create/', CreateWarehouseMovementsInvoiceView.as_view(), name='ware_move_create'),
    path('warehouse-movements-detail/<int:pk>/', WarehouseMovementsInvoiceUpdateView.as_view(), name='ware_move_update'),
    path('warehouse-movements-delete-<int:pk>/', delete_warehouse_movements_invoice_view, name='ware_move_delete'),
    path('ware-move-add-products/<int:pk>/', validate_add_products_view, name='validate_add_products'),
    path('ware-move-delete-item/<int:pk>/', delete_ware_move_item, name='ware_move_item_delete'),


    path('invoice-items-list/', InvoiceItemListView.as_view(), name='invoice_item_list_view'),

    # autocomplete
    path('autocomplete-vendor/', VendorAutocomplete.as_view(), name='vendor_autocomplete'),
    
]
