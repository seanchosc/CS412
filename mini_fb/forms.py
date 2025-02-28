from django import forms
from .models import Profile, StatusMessage # Import models

class CreateProfileForm(forms.ModelForm):
    ''' A form to create a Profile and add it to DB'''
    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['firstName', 'lastName', 'city', 'emailAddress', 'profileImageURL']

    # list of fields that this form should set (i.e., all of the data attributes of the Profile class) #
    firstName = forms.TextField(blank=False, required=True) # person's first name attribute
    lastName = forms.TextField(blank=False, required=True) # person's last name attribute
    city = forms.TextField(blank=False, required=True) # person's city attribute
    emailAddress = forms.TextField(blank=False, required=True) # person's email attribute
    profileImageURL = forms.TextField(blank=False) # person's profile image url attribute

