## Create a Model 
#
# mini_fb/models.py
# Define the data objects for our application
#
from django.db import models
from django.templatetags.static import static # import static to use my custom photo in images for butter cat
from django.urls import reverse # import reverse for get_absolute_url
# Create your models here.
class Profile(models.Model):
    '''Encapsulate the idea of a Profile.'''

    # data attributes of a Profile:
    firstName = models.TextField(blank=False) # person's first name attribute
    lastName = models.TextField(blank=False) # person's last name attribute
    city = models.TextField(blank=False) # person's city attribute
    emailAddress = models.TextField(blank=False) # person's email attribute
    #profileImageURL = models.TextField(blank=False) # person's profile image url attribute
    image_file = models.ImageField(blank=True) # NEW IMAGE FIELD (an actual image)
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.firstName} {self.lastName}' # return as string their full name (no middle name attribute) 
    
    def get_status_messages(self):
        ''' accessor method to obtain all status messages for this Profile '''
        messages = StatusMessage.objects.filter(profile = self) # filter the status messages
        return messages
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    
class StatusMessage(models.Model):
    '''models the data attributes of Facebook status message'''
    timestamp = models.DateTimeField(auto_now=True) # the time at which this status message was created/saved
    message = models.TextField(blank=False) # the text of the status message
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE) # the foreign key to indicate the relationship to the Profile of the creator of this message
    
    def __str__(self):
        ''' Return a string representation of this StatusMessage object '''
        return f'{self.message}, {self.timestamp} ~ {self.profile}'
    def get_images(self):
        return Image.objects.filter(statusimage__status_message=self)
class Image(models.Model):
    ''' encapsulates the idea of an image file (not a URL) that is stored in the Django media directory'''
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE) # # the foreign key to indicate the relationship to the Profile of the uploader of this image
    image_file = models.ImageField(blank=True) # the ImageField being stored
    timestamp = models.DateTimeField(auto_now = True) # the time at which this image was uploaded
    caption = models.TextField(max_length=255, blank=True) # optional caption

class StatusImage(models.Model):
    ''' encapsulates the idea of a StatusImage'''
    image = models.ForeignKey("Image", on_delete=models.CASCADE) # Images that relate to a StatusMessage
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE) # StatusMessage to which an Image is related

