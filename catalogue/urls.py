from django.urls import path

from .views import (HomepageView, ProductClassListView, ProductClassCreateView,
                    ProductListView, ProductCreateView, ProductUpdateView, delete_product_view,
                    CategoryListView, CategoryCreateView, CategoryUpdateView, category_delete_view,
                    product_analysis_view
                    )
from .action_views import (create_storage_form_view, create_product_ingredient_view, class_copy_product_view,
                           ProductIngredientUpdateView, ingredient_delete_view, ProductStorageUpdateView, delete_product_storage_view,
                           popup_vendor, popup_storage, popup_category
                           )
app_name = 'catalogue'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('product-class-list/', ProductClassListView.as_view(), name='product_class_list_view'),
    path('product-class-create/', ProductClassCreateView.as_view(), name='product_class_create'),
    path('product/analysis/<int:pk>/', product_analysis_view, name='product_analysis'),

    path('edit-views/product/list/', ProductListView.as_view(), name='product_list'),
    path('edit-views/product/create/', ProductCreateView.as_view(), name='product_create'),
    path('edit-views/product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('edit-views/product-delete/<int:pk>/', delete_product_view, name='product_delete'),
    path('product-storage-update/<int:pk>/', ProductStorageUpdateView.as_view(), name='product_storage_update'),
    path('product-storage-delete/<int:pk>', delete_product_storage_view, name='delete_product_storage'),

    path('category-list-view/', CategoryListView.as_view(), name='category_list'),
    path('category-create/', CategoryCreateView.as_view(), name='category_create'),
    path('category-update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/<int:pk>/', category_delete_view, name='category_delete'),

    # action views
    path('product-storage-create/<int:pk>/', create_storage_form_view, name='action_product_storage_create'),
    path('product-ingredient-create/<int:pk>/', create_product_ingredient_view, name='action_product_ingredient_create'),
    path('copy-product/<int:pk>/', class_copy_product_view, name='copy_product'),
    path('update/product-ingredient/<int:pk>/', ProductIngredientUpdateView.as_view(), name='update_ingredient'),
    path('delete/product-ingredient/<int:pk>/', ingredient_delete_view, name='delete_ingredient',),

    path('popup/add-vendor/', popup_vendor, name='popup_vendor'),
    path('popup/add-storage/', popup_storage, name='popup_storage'),
    path('popup/add-category/', popup_category, name='popup_category'),

]
