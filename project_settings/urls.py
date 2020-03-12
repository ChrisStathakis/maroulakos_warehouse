from django.urls import path
from .views import (HomepageView,
                    StorageListView, StorageCreateView, StorageUpdateView, delete_storage_view
                    )
app_name = 'settings'

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
    path('storage-list/', StorageListView.as_view(), name='storage_list'),
    path('storage-create/', StorageCreateView.as_view(), name='storage_create'),
    path('storage-update/<int:pk>/', StorageUpdateView.as_view(), name='storage_update'),
    path('storage-delete/<int:pk>/', delete_storage_view, name='storage_delete'),

]
