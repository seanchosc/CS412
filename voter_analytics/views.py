# voter_analytics/views.py
#
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Voter # import the voter mdel

class ResultsListView(ListView):
    '''View to display voter information'''

    template_name = 'voter_analytics/voter.html'
    model = Voter
    context_object_name = 'voter'

    def get_queryset(self):
        
        # limit results to first 25 records (for now)
        qs = super().get_queryset()
        return qs[:25]