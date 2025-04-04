from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.VoterListView.as_view(), name='home'), # display voter view
    path(r'results', views.VoterListView.as_view(), name='voter_list'), # display voter view
]   