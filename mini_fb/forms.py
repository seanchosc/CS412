from django import forms
from .models import Profile, StatusMessage # Import models, StatusMessages 

class CreateProfileForm(forms.ModelForm):
    ''' A form to create a Profile and add it to DB'''
    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['firstName', 'lastName', 'city', 'emailAddress', 'image_file'] # updated image field variable

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Status Message to the database'''
    class Meta:
        ''' associate this form with the StatusMessage model; select fields '''
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    ''' A form to update a Profile to the database'''
    class Meta:
        ''' associate this form with the Profile model; select fields'''
        model = Profile
        fields = ['city', 'emailAddress', 'image_file']


