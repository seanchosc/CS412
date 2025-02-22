## Create app-specific URL:
# mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfilesView, BaseView, ShowProfilePageView # our view class definition 

urlpatterns = [
    # map the URL (empty string) to the view
    path('', BaseView.as_view(), name='base'), # base view
    path('show_all_profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'), # show all profiles view
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'), # show profile page view
]