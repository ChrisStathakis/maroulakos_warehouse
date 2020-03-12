from django.urls import path

from .views import DashboardHomepageView


urlpatterns = [
    path('', DashboardHomepageView.as_view(), name='homepage')
]