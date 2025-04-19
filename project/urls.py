## Create app-specific URL:
# project/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views    ## NEW
from .views import * # import everything from views
urlpatterns = [
    # map the URL (empty string) to the view
    path('dashboard/<int:pk>/', ShowUserDashboardView.as_view(), name='user_dashboard'),
]