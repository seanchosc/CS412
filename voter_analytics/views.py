# voter_analytics/views.py
#
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Voter # import the voter mdel
from django.views.generic.detail import DetailView #import detailview for voter detail view

import math
import plotly
import plotly.graph_objs as go
# BASE VIEW
class BaseView(ListView):
    ''' base view'''
    model = Voter # retrieve objects of type Voter from the database
    template_name = 'voter_analytics/base.html' # base template
    context_object_name = 'voter' # how to find the data in the template file

class VoterListView(ListView):
    '''View to display voter information'''

    template_name = 'voter_analytics/voter.html' # voter template
    model = Voter # retrieve objects of type Voter from the database
    context_object_name = 'voters' # how to find the data in the template file
    paginate_by = 25    # 25 records per page

    def get_queryset(self):
        voters = super().get_queryset()
        if 'affiliation' in self.request.GET:
            party = self.request.GET['affiliation']
            if party:
                voters = voters.filter(affiliation=party)
        if 'voterScore' in self.request.GET:
            score = self.request.GET['voterScore']
            if score:
                voters = voters.filter(voterScore=score)
        if 'minYOB' in self.request.GET:
            yob = self.request.GET['minYOB']
            if yob:
                voters = [v for v in voters if v.dob[:4] == yob]
        if 'maxYOB' in self.request.GET:
            yob = self.request.GET['maxYOB']
            if yob:
                voters = [v for v in voters if v.dob[:4] == yob]
        if 'v20' in self.request.GET:
            voters = voters.filter(v20=True)
        if 'v21t' in self.request.GET:
            voters = voters.filter(v21t=True)
        if 'v21p' in self.request.GET:
            voters = voters.filter(v21p=True)
        if 'v22' in self.request.GET:
            voters = voters.filter(v22=True)   
        if 'v23' in self.request.GET:
            voters = voters.filter(v23=True)   
        return voters
    
class VoterDetailView(DetailView):
    ''' show a page for a single Voter record '''
    model = Voter
    template_name = 'voter_analytics/single_voter.html'
    context_object_name = 'voter'

class GraphsView(ListView):
    ''' view for voter information in graphs '''

