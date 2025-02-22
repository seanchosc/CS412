## Create View
# mini_fb/views.py
# Define the views for the blog app:
from django.shortcuts import render
from .models import Profile # import Profile model
from django.views.generic import ListView, DetailView #ListView for Base and SAP, Detail for ShowProfile

# BASE VIEW
class BaseView(ListView):
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/base.html' # base template
    context_object_name = 'profiles' # how to find the data in the template file

#SHOW ALL PROFILES VIEW
class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html' # show_all_profiles template
    context_object_name = 'profiles' # how to find the data in the template file

### Create DetailView to show one article by its PK:
# mini_fb/views.py
#SHOW PROFILE PAGE VIEW:
class ShowProfilePageView(DetailView):
    '''Show the details for one profile.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_profile.html' # show_profile_page template
    context_object_name = 'profile' # how to find the data in the template file
