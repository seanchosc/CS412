from django import forms
from .models import Profile

class CreateProfileForm(forms.Model):
    ''' A form to create a Profile and add it to DB'''
    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['firstName', 'lastName', 'city', 'emailAddress', 'profileImageURL']
        