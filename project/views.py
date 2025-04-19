from django.shortcuts import render


from django.views.generic import DetailView
from .models import Profile, Event, EventCollaborator, Collaborator, EventInvite

# Create your views here.

class ShowUserDashboardView(DetailView):
    '''Show a user's dashboard'''
    model = Profile
    template_name = 'project/user_dashboard.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_object()

        # Events created by the user
        created_events = Event.objects.filter(event_creator=profile)
        # Events where the user is a collaborator
        event_collaborator = EventCollaborator.objects.filter(collaborator=profile)
        events = [event_collaborator_object.event for event_collaborator_object in event_collaborator]
        # Combine
        all_events = list(created_events) + events

        # Pending event invites
        pending_event_invites_received= EventInvite.objects.filter(invitee=profile, invite_status='pending')
        pending_event_invites_sent = EventInvite.objects.filter(inviter=profile, invite_status='pending')

        # Accepted collaborators
        sent_accepted = Collaborator.objects.filter(inviter=profile, invite_status='accepted')
        received_accepted = Collaborator.objects.filter(invitee=profile, invite_status='accepted')
        accepted_collaborators = list(sent_accepted) + list(received_accepted)
        # Pending collaborators
        pending_collab_invites_sent = Collaborator.objects.filter(inviter=profile, invite_status='pending')
        # Pending invites received
        pending_collab_invites_received = Collaborator.objects.filter(invitee=profile, invite_status='pending')


        context['events'] = all_events
        context['pending_event_invites_received'] = pending_event_invites_received
        context['pending_event_invites_sent'] = pending_event_invites_sent

        context['collaborators'] = accepted_collaborators
        context['pending_collab_invites_sent'] = pending_collab_invites_sent
        context['pending_collab_invites_received'] = pending_collab_invites_received

        return context
