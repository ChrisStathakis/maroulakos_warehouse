from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('dashboard.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('project-settings/', include('project_settings.urls')),
    path('warehouse/', include('warehouse.urls')),
    path('point-of-sale/', include('point_of_sale.urls')),
]
