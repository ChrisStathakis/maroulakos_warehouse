from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),

    path('', include('dashboard.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('project-settings/', include('project_settings.urls')),
    path('warehouse/', include('warehouse.urls')),
    path('point-of-sale/', include('point_of_sale.urls')),
    path('costumers/', include('costumers.urls')),
    path('payroll/', include('payroll.urls')),
    path('analysis/', include('analysis.urls')),
    path('offsshores/', include('OffsShoreCostumers.urls')),

]
