from django.urls import path

from .views import (HomepageView, ProductClassListView,
                    ProductListView, ProductCreateView, ProductUpdateView, delete_product_view
                    )

app_name = 'catalogue'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('product-class-list/', ProductClassListView.as_view(), name='product_class_list_view'),

    path('edit-views/product/list/', ProductListView.as_view(), name='product_list'),
    path('edit-views/product/create/', ProductCreateView.as_view(), name='product_create'),
    path('edit-views/product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('edit-views/product-delete/<int:pk>/', delete_product_view, name='product_delete'),


]
