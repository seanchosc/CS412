from django.contrib import admin

# Register your models here.
from .models import (Profile, Event, EventPostMedia, EventPost, Collaborator, EventInvite, EventCollaborator)
admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(EventPost)
admin.site.register(EventPostMedia)
admin.site.register(Collaborator)
admin.site.register(EventInvite)
admin.site.register(EventCollaborator)