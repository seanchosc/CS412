## Create View
# mini_fb/views.py
# Define the views for the blog app:
from django.shortcuts import render, redirect
from .models import Profile, Image, StatusImage, StatusMessage # import these models from models.py
from django.views.generic import ListView, DetailView, CreateView # ListView for Base and SAP, Detail for ShowProfile, CreateView for CreateProfileView
from django.views.generic import View # For AddFriendView
from django.views.generic.edit import UpdateView, DeleteView # UpdateView for UpdateProfileView, DeleteView for DeleteStatusMessageView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm # Import the create profile, create status message, and update profile forms from forms, 
from django.urls import reverse 
# Assignment 9
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW for requiring user to be logged in
from django.views.generic import TemplateView # For logout confirmation redirect page
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW

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
    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
        return super().dispatch(request, *args, **kwargs)
    
### Create DetailView to show one Profile by its PK:
# mini_fb/views.py
#SHOW PROFILE PAGE VIEW:
class ShowProfilePageView(DetailView):
    '''Show the details for one profile.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_profile.html' # show_profile_page template
    context_object_name = 'profile' # how to find the data in the template file
    
### Create Profile View ###
class CreateProfileView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''
    form_class = CreateProfileForm # use the CreateProfileForm class in forms
    template_name = 'mini_fb/create_profile_form.html' # show create_profile_form template
    context_object_name = 'form' # how to find the data in the template file
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        print(f'CreateProfileView: form.cleaned_data={form.cleaned_data}')

        # find the logged in user
        user = self.request.user
        print(f"CreateProfileView user={user} profile.user={user}")

        # attach user to form instance (Profile object):
        form.instance.user = user

		# delegate work to the superclass version of this method
        return super().form_valid(form)


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a new status message and save it to the database.'''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html' # show create status form template
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        ''' OLD IMPLEMENTATION

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        
        '''

        ### NEW IMPLEMENTATION
        profile = Profile.objects.get(user=self.request.user)

        # add this profile into the context dictionary:
        context['profile'] = profile
        return context
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Status Message.'''

        ''' OLD IMPLEMENTATION

        # create and return a URL:
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Profile
        return reverse('show_profile', kwargs={'pk':pk})   

        '''

        ### NEW IMPLEMENTATION
        profile = Profile.objects.get(user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Status Message
        object before saving it to the database.
        '''
        
		# instrument our code to display form fields: 
        print(f"CreateStatusMessageView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # find the logged in user
        user = self.request.user
        print(f"CreateStatusMessageView user={user} profile.user={user}")

        # attach user to form instance (Profile object):
        form.instance.user = user

        ''' OLD IMPLEMENTATION

        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this profile to the status message
        form.instance.profile = profile # set the FK

        ''' 

        ### NEW IMPLEMENTATION
        profile = Profile.objects.get(user=self.request.user)
        
        # Assign the message to the user
        form.instance.profile = profile

        # save the status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for file in files: # for each file
            # Create an Image object, and set the file into the Image‘s ImageField attribute
            image = Image(profile=profile, image_file=file)
            image.save()
            print(f"Image {image.id} saved")
            # Create and save a StatusImage object that sets the foreign keys of the StatusMessage and the Image objects
            status_image = StatusImage(image=image, status_message=sm)
            # save the Image object to the database
            status_image.save()
            print(f"StatusImage {status_image.id} saved")
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    ''' A view to update a Profile and save it to the database '''
    model = Profile
    form_class = UpdateProfileForm #UpdateProfileForm class in forms.py
    template_name = 'mini_fb/update_profile_form.html' # show update_profile_form template
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def form_valid(self, form):
        '''
        Handle the form submission to update a Profile object.
        '''
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')
                
        # find the logged in user
        user = self.request.user
        print(f"UpdateProfileView user={user} profile.user={user}")

        # attach user to form instance (Profile object):
        form.instance.user = user
        
        return super().form_valid(form)
    def get_object(self):
        ''' uses the logged in user (self.request.user) and 
        the object manager (Profile.objects) to locate and 
        return the Profile corresponding to this User '''
        return Profile.objects.get(user=self.request.user)
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a status message and remove it from the database.'''

    template_name = "mini_fb/delete_status_form.html" # show delete_status_form template
    model = StatusMessage # use StatusMessage model
    context_object_name = 'status_message' # set context variable as status_message
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_success_url(self):
        '''Provide a URL to redirect to after deleting a Status Message.'''

        # get the pk for this comment
        pk = self.kwargs['pk']
        status_message = StatusMessage.objects.get(pk=pk)

        # find the article to which this Comment is related by FK
        profile = status_message.profile

        # reverse to show the profile page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''A view to handle updating an existing StatusMessage.'''
    template_name = 'mini_fb/update_status_form.html'  # this template you'll create in the next step
    model = StatusMessage
    context_object_name = 'status_message'
    form_class = UpdateStatusMessageForm
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_success_url(self):
        '''After updating, redirect to the associated profile.'''
        # get the pk for this comment
        pk = self.kwargs['pk']
        status_message = StatusMessage.objects.get(pk=pk)

        # find the article to which this Comment is related by FK
        profile = status_message.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})
    def form_valid(self, form):
        '''
        Handle the form submission to update a StatusMessage object.
        '''
        print(f'UpdateStatusMessageView: form.cleaned_data={form.cleaned_data}')
                
        # find the logged in user
        user = self.request.user
        print(f"UpdateStatusMessageView user={user} profile.user={user}")

        # attach user to form instance (Profile object):
        form.instance.user = user
        
        return super().form_valid(form)
class AddFriendView(LoginRequiredMixin, View):
    ''' A view to handle adding a friend'''
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')  
    def dispatch(self, request, *args, **kwargs):
        ''' we can read the URL parameters (from self.kwargs), use the object manager 
        to find the requisite Profile objects, and then call 
        the Profile‘s add_friend method (from step 2). 
        Finally, we can redirect the user back to the profile page'''

        ''' OLD IMPLEMENTATION
        # read the URL paramters
        pk = self.kwargs['pk']
        other_pk = self.kwargs['other_pk']

        # find the requisite Profile objects
        profile = Profile.objects.get(pk=pk)
        other_profile = Profile.objects.get(pk=other_pk)        
        '''

        ### NEW IMPLEMENTATION
        # read the URL parameters
        other_pk = self.kwargs['other_pk']

        # find the requisite Profile objects
        profile = Profile.objects.get(user=request.user)
        other_profile = Profile.objects.get(pk=other_pk)    

        # call the Profile's add_friend method
        profile.add_friend(other_profile)

        # redirect the user back to the profile page
        return redirect(reverse('show_profile', kwargs={'pk': profile.pk}))
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    ''' view for showing friend suggestions '''
    model = Profile # retrieve objects of type Profile from the database
    template_name = "mini_fb/friend_suggestions.html" #friend_suggestion.html template
    context_object_name = 'profile' # how to find the data in the template file
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data(**kwargs)

        ''' OLD IMPLEMENTATION 
        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=self.kwargs['pk'])
    '''
        ### NEW IMPLEMENTATION:
        profile = Profile.objects.get(user=self.request.user)

        # add this profile into the context dictionary:
        context['profile'] = profile

        # add friend suggestions to context
        context['friends'] = profile.get_friend_suggestions()
        return context
    def get_object(self):
        ''' uses the logged in user (self.request.user) and 
        the object manager (Profile.objects) to locate and 
        return the Profile corresponding to this User '''
        return Profile.objects.get(user=self.request.user)
class ShowNewsFeedView(DetailView):
    ''' view for showing news feed'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/news_feed.html' #news_feed.html template
    context_object_name = 'profile' # how to find the data in the template file
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)  # calling the superclass method
        profile = self.get_object() # retrieve the self object
        # add news feed to context
        context['news_feed'] = profile.get_news_feed()
        return context
    def get_object(self):
        ''' uses the logged in user (self.request.user) and 
        the object manager (Profile.objects) to locate and 
        return the Profile corresponding to this User '''
        return Profile.objects.get(user=self.request.user)
class LogoutRedirectView(TemplateView):
    ''' View for being redirected to logout confirmation page'''
    template_name = 'mini_fb/logged_out.html' ## show the logged_out template 
class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''
    template_name = 'mini_fb/register.html' # show the register template
    form_class = UserCreationForm # use the imported UserCreationForm class
    model = User # use the import User model
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')