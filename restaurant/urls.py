from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [ 
    path(r'', views.main, name="main"), # New base path
    path(r'main/', views.main, name="main"), # New main path
    path(r'order/', views.order, name="order"), # New order path
    path(r'confirmation/', views.confirmation, name="confirmation"), # New confirmation path
    path(r'submit', views.submit, name = "submit"), # New submit path
]