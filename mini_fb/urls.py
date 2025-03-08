## Create app-specific URL:
# mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfilesView, BaseView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView # our view class definition 
from .views import UpdateProfileView # update profile view in views
urlpatterns = [
    # map the URL (empty string) to the view
    path('', BaseView.as_view(), name='base'), # base view
    path('show_all_profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'), # show all profiles view
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'), # show profile page view
    path('profile/create_profile/', CreateProfileView.as_view(), name='create_profile'), # show create profile view
    path('profile/<int:pk>/create_status/',CreateStatusMessageView.as_view(), name='create_status' ), # show create status message view
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile") # show update profile view
]