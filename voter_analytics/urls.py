from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.BaseView.as_view(), name='home'), # display base view
    path(r'voters', views.VoterListView.as_view(), name='voters_list'), # display voter view
]   