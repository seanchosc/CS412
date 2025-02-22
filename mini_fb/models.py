## Create a Model 
#
# mini_fb/models.py
# Define the data objects for our application
#
from django.db import models
from django.templatetags.static import static # import static to use my custom photo in images for butter cat

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of a Profile.'''

    # data attributes of a Profile:
    firstName = models.TextField(blank=False) # person's first name attribute
    lastName = models.TextField(blank=False) # person's last name attribute
    city = models.TextField(blank=False) # person's city attribute
    emailAddress = models.TextField(blank=False) # person's email attribute
    profileImageURL = models.TextField(blank=False) # person's profile image url attribute
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.firstName} {self.lastName}' # return as string their full name (no middle name attribute) 