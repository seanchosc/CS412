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
    def get_friends(self):
        '''return a list of friend's profiles'''
        friends1 = Friend.objects.filter(profile1=self)    # get friends for profile1
        friends2 = Friend.objects.filter(profile2=self) # get fruebds for profile2
        friends = []    # friends list

        for friend in friends1: # for each friendship
            friends.append(friend.profile2) # self is profile1
        for friend in friends2: # for each friendship
            friends.append(friend.profile1) # self is profile2
        return friends
    def add_friend(self, other):
        ''' takes a paramter other, which refers to another Profile instance, and adds a Friend relation with self'''
        if other == self:   # dont want to friend yourself
            return "Error: Can't friend yourself."
        friends1 = Friend.objects.filter(profile1=self, profile2=other)
        friends2 = Friend.objects.filter(profile1=other, profile2=self)
        if (friends1.count() == 0) and (friends2.count() == 0): # if not friends with each other already
            Friend.objects.create(profile1=self, profile2=other)
        else:
            return "Error: Already friends."
        
    def get_friend_suggestions(self):
        ''' returns a list (or QuerySet) of possible friends for a Profile '''
        friends = self.get_friends()    # current friends
        friends_pk = [friend.pk for friend in friends] # list of each friends pk

        # suggested friends excludes people already friends and the self profile
        suggested_friends = Profile.objects.exclude(pk=self.pk).exclude(pk__in=friends_pk)

        return suggested_friends

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

class Friend(models.Model):
    ''' encapsulates the idea of an edge connecting two nodes 
    within the social network (e.g., two Profiles that are friends with each other)'''
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1") # first person that relates to a Friend relationship
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2") # second person that relates to a Friend relationship
    timestamp = models.DateTimeField(auto_now_add=True) # timestamp of when the friend relationship was created    
    def __str__(self):
        '''view this relationship as a string representation'''
        return f"{self.profile1} and {self.profile2} are friends"