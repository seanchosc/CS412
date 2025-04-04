# voter_analytics/views.py
#
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Voter # import the voter mdel

# BASE VIEW
class BaseView(ListView):
    model = Voter # retrieve objects of type Voter from the database
    template_name = 'voter_analytics/base.html' # base template
    context_object_name = 'voter' # how to find the data in the template file

class VoterListView(ListView):
    '''View to display voter information'''

    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'

    def get_queryset(self):
        
        # limit results to first 25 records (for now)
        qs = super().get_queryset()
        return qs[:25]