## Create app-specific URL:
# mini_fb/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views    ## NEW
from .views import * # import everything from views
urlpatterns = [
    # map the URL (empty string) to the view
    path('', BaseView.as_view(), name='base'), # base view
    path('show_all_profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'), # show all profiles view
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'), # show profile page view
    path('profile/create_profile/', CreateProfileView.as_view(), name='create_profile'), # show create profile view
    path('profile/<int:pk>/create_status/',CreateStatusMessageView.as_view(), name='create_status' ), # show create status message view
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"), # show update profile view
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'), # show DeleteStatusMessage view
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'), # show update status message view
    path('profile/<int:pk>/add_friend/<int:other_pk>/', AddFriendView.as_view(), name='add_friend'), # show add friend view
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'), #show ShowFriendSuggestionsView
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'), # show news feed view
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), ## show login template when logging in
	path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), ## show show all template when logging out
]