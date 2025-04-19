from django.db import models

# Import built in django User model #
from django.contrib.auth.models import User

# Import Coalesce to sort event times by start and end time
from django.db.models.functions import Coalesce

# Create your models here.


# Profile model # 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')
    first_name = models.TextField()
    last_name = models.TextField()
    email_address = models.TextField(blank=False) # person's email attribute
    profile_photo = models.ImageField(blank=True)
    timezone = models.CharField(max_length=10)
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}' # return as string their full name (no middle name attribute)
    def get_name(self):
        return f"{self.first_name} {self.last_name}"
    def add_collaborator(self, other, collaborator_type):
        if other == self:
            return "Error: Can't collaborate with yourself."
        profile1 = self.profile
        profile2 = other.profile
        collaborator1 = Collaborator.objects.filter(inviter=profile1, invitee=profile2, collaborator_type=collaborator_type)
        collaborator2 = Collaborator.objects.filter(inviter=profile2, invitee=profile1, collaborator_type=collaborator_type)

        if collaborator1.exists() or collaborator2.exists():
            return "Error: Already collaborators or pending request exists."
        # Otherwise, create collaborator relationship
        Collaborator.objects.create(inviter=profile1,invitee=profile2,collaborator_type=collaborator_type,invite_status='pending')
        return "Collaborator request sent!"
    def accept_collaborator(self, other, collaborator_type):
        profile1 = other.profile
        profile2 = self.profile
        pending_invites = Collaborator.objects.filter(inviter=profile1, invitee=profile2, collaborator_type=collaborator_type, invite_status='pending')
        if pending_invites.exists():
            collaborator = pending_invites.first()
            collaborator.invite_status = 'accepted'
            collaborator.save()
            return "Collaborator request accepted."
        else:
            return "No pending collaborator request."
    def add_event_collaborator(self, event, other, role='attendee'):
        """Send an event invitation to another user (friend/work contact)"""
        profile1 = self.profile
        profile2 = other.profile

        if profile1 == profile2:
            return "Error: Can't invite yourself to an event."

        # Prevent duplicates
        existing_invite = EventInvite.objects.filter(event=event, invitee=profile2)
        existing_collab = EventCollaborator.objects.filter(event=event, collaborator=profile2)

        if existing_invite.exists():
            return "Invite already sent for this event."
        if existing_collab.exists():
            return "User is already a collaborator for this event."

        # Send the invite
        EventInvite.objects.create(event=event, inviter=profile1, invitee=profile2, invite_status='pending')
        return "Event invite sent!"

    def accept_event_collaborator(self, event):
        """Accept an invitation to an event and become a collaborator"""
        profile = self.profile
        pending_invite = EventInvite.objects.filter(event=event, invitee=profile, invite_status='pending')

        if pending_invite.exists():
            invite = pending_invite.first()
            invite.invite_status = 'accepted'
            invite.save()

            EventCollaborator.objects.create(event=event, collaborator=profile, role='attendee')
            return "Event invite accepted!"
        else:
            return "No pending invite."

# Event Query Set #
class EventQuerySet(models.QuerySet):

    # function to order events based on time for edge cases like when event_start_time is given but not end time
    def ordered_by_event_time(self):
        return self.annotate(event_time=Coalesce('event_start_time', 'event_end_time')).order_by('event_date', 'event_time')
# Event Model # 
class Event(models.Model):

    EVENT_TYPES = [('self', 'Self'), ('friends', 'Friends'), ('work', 'Work')] # Types of events
    event_title = models.CharField(max_length=60) # Event title
    event_description = models.TextField() # Event description, text field because we will allow long event descriptions
    event_start_time = models.TimeField(null = True, blank = True) # Event start time, optional
    event_end_time = models.TimeField(null = True, blank= True) # Event end time, optional
    event_date = models.DateField() # Event date, this is required
    event_creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_events') # Creator of the event
    event_type = models.CharField(max_length=7, choices=EVENT_TYPES) # type of event

    objects = EventQuerySet.as_manager() # to use custom event ordering function

    def __str__(self):
        # Returns the string representation of an event depending on which date/time fields were given
        if self.event_start_time and self.event_end_time:
            return f'{self.event_title} ({self.event_start_time}~{self.event_end_time} on {self.event_date})'
        elif self.event_start_time:
            return f'{self.event_title} (Starts at: {self.event_start_time} on {self.event_date})'
        elif self.event_end_time:
            return f'{self.event_title} (Ends at: {self.event_end_time} on {self.event_date})'
        else:
            return f'{self.event_title} on {self.event_date}'
        
    class Meta:
        # Meta class to provide ordering details"
        ordering = ['event_date', 'event_start_time'] # Default sorting behavior, but will use Coalesce when needed 
                                                      # (if event_start_time is given but not end time_)
        
class EventPost(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    post_author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_text_content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Post by: {self.post_author.get_name()}, at {self.timestamp}'
class EventPostMedia(models.Model):
    post = models.ForeignKey(EventPost, on_delete=models.CASCADE, related_name='media')
    post_media = models.ImageField()
    def __str__(self):
        return f"Media Content for Post {self.post.id} by {self.post.post_author.get_name()}"

class Collaborator(models.Model):
    COLLABORATOR_TYPES = [('friend', 'Friend'), ('work', 'Work')]
    INVITE_STATUSES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')]
    inviter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_collaborator_invites')
    invitee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_collaborator_invites')
    invite_status = models.CharField(max_length=8, choices=INVITE_STATUSES, default='pending')
    collaborator_type = models.CharField(max_length=6, choices=COLLABORATOR_TYPES)
    def __str__(self):
        inviter_name = self.inviter.get_name()
        invitee_name = self.invitee.get_name()
        if self.invite_status == 'pending':
            return f"{inviter_name}'s collaboration invite to {invitee_name} of type [{self.collaborator_type}] is PENDING"
        elif self.invite_status == 'accepted':
            return f"{inviter_name}'s collaboration invite to {invitee_name} of type [{self.collaborator_type}] is ACCEPTED"
        else:
            return f"{inviter_name}'s collaboration invite to {invitee_name} of type [{self.collaborator_type}] is REJECTED"

class EventInvite(models.Model):
    INVITE_STATUSES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='invites')
    inviter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_event_invites')
    invitee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_event_invites')
    invite_status = models.CharField(max_length=10, choices=INVITE_STATUSES, default='pending')
    def __str__(self):
        return f"{self.inviter.get_name()} invited {self.invitee.get_name()} to '{self.event.event_title}' [{self.invite_status}]"
class EventCollaborator(models.Model):
    ROLE_TYPES = [('attendee', 'Attendee'),('editor', 'Editor')]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='collaborators')
    collaborator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_TYPES, default='attendee')
    def __str__(self):
        return f"{self.collaborator.get_name()} ({self.role}) is attending event: {self.event.event_title}"
