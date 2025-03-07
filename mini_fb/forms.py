from django import forms
from .models import Profile, StatusMessage # Import models, StatusMessages 

class CreateProfileForm(forms.ModelForm):
    ''' A form to create a Profile and add it to DB'''
    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['firstName', 'lastName', 'city', 'emailAddress', 'image_file'] # updated image field variable

    # list of fields that this form should set (i.e., all of the data attributes of the Profile class) #
    #firstName = forms.CharField(required=True, label = "First name:") # person's first name attribute
    #lastName = forms.CharField(required=True, label = "Last name:") # person's last name attribute
    #city = forms.CharField(required=True, label = "City") # person's city attribute
    #emailAddress = forms.CharField(required=True, label = "Email address:") # person's email attribute
    #profileImageURL = forms.CharField(required=True, label = "Profile photo URL:") # person's profile image url attribute

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Status Message to the database'''
    class Meta:
        ''' associate this form with the StatusMessage model; select fields '''
        model = StatusMessage
        fields = ['message']
    # list of fields that this form should set #
    #message = forms.CharField(max_length=200, required=True, label = "Your new message:",
                              #widget=forms.Textarea(attrs={"rows": 4, "cols": 50})) # larger text box

