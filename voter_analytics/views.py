# voter_analytics/views.py
#
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Voter # import the voter mdel
from django.views.generic.detail import DetailView #import detailview for voter detail view

### FOR GRAPHS
import math
import plotly
import plotly.graph_objs as go

### FOR SLICING BIRTH YEAR
from django.db.models.functions import Substr

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
        # get birth year        
        voters = voters.annotate(yob=Substr('dob', 1, 4))
        if 'minYOB' in self.request.GET:
            yob = self.request.GET['minYOB']
            if yob:
                # greater than or equal
                voters = voters.filter(yob__gte=yob)
        if 'maxYOB' in self.request.GET:
            yob = self.request.GET['maxYOB']
            if yob:
                # less than or equal
                voters = voters.filter(yob__lte=yob)
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
    model = Voter # retrieve objects of type Voter from the database
    template_name = 'voter_analytics/single_voter.html' # single_voter template
    context_object_name = 'voter'
    

class GraphsListView(ListView):
    ''' view for voter information in graphs '''
    model = Voter # retrieve objects of type Voter from the database
    template_name = 'voter_analytics/graphs.html' # graphs template
    def get_queryset(self):
        ''' override get_queryset method'''
        voters = super().get_queryset()
        if 'affiliation' in self.request.GET:
            party = self.request.GET['affiliation']
            if party:
                voters = voters.filter(affiliation=party)
        if 'voterScore' in self.request.GET:
            score = self.request.GET['voterScore']
            if score:
                voters = voters.filter(voterScore=score)
        # get birth year        
        voters = voters.annotate(yob=Substr('dob', 1, 4))
        if 'minYOB' in self.request.GET:
            yob = self.request.GET['minYOB']
            if yob:
                # greater than or equal
                voters = voters.filter(yob__gte=yob)
        if 'maxYOB' in self.request.GET:
            yob = self.request.GET['maxYOB']
            if yob:
                # less than or equal
                voters = voters.filter(yob__lte=yob)
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
    def get_context_data(self, **kwargs):
        ''' get the context data'''

        context = super().get_context_data(**kwargs)

        # Get all Voters as query set
        voters = self.get_queryset()

######### START: DISTRIBUTION OF VOTERS BY AGE #########
        # count which years voters were born
        countAge = {}
        for voter in voters:
            if voter.dob:
                year = voter.dob[:4]
                countAge[year] = countAge.get(year, 0) + 1
        # create the graph as Bar chart
        xAge = sorted(countAge.keys())
        yAge = [countAge[year] for year in xAge]

        # generate the Bar chart
        figAge = go.Bar(x=xAge, y=yAge)
        titleAge = "Voter Distribution by Year of Birth"

        # obtain the graph as an HTML div"
        graph_div_age = plotly.offline.plot(
            {"data": [figAge], "layout_title_text": titleAge},
            auto_open=False,
            output_type="div"
        )

        # send div as template context variable
        context['graph_div_age'] = graph_div_age

        # count sample size
        nAge = sum(1 for v in voters if v.dob)
        # send nAge as template context variable
        context['nAge'] = nAge
#########                   END                  #########

######### START: DISTRIBUTION OF VOTERS BY PARTY #########
        countParty = {}
        for voter in voters:
            if voter.affiliation:
                aff = voter.affiliation.strip()
                countParty[aff] = countParty.get(aff, 0) + 1
        # create the graph as Pie chart
        xParty = sorted(countParty.keys())
        yParty = [countParty[party] for party in xParty]
        # generate the Pie chart
        figParty = go.Pie(labels=xParty, values=yParty)
        titleParty = "Voter Distribution by Party Affiliation"
        # obtain the graph as an HTML div"
        graph_div_party = plotly.offline.plot(
            {"data": [figParty], "layout_title_text": titleParty},
            auto_open=False,
            output_type="div"
        )
        # send div as template context variable
        context['graph_div_party'] = graph_div_party

        # count sample size
        nParty = sum(1 for v in voters if v.affiliation)
        # send nParty as template context variable
        context['nParty'] = nParty
#########                   END                  #########

######### START: DISTRIBUTION OF VOTERS BY PREVIOUS ELECTIONS #########
        elections = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        countElections = {election: 0 for election in elections}
        for voter in voters:
            if voter.v20:
                countElections['2020 State']+=1
            if voter.v21t:
                countElections['2021 Town']+=1
            if voter.v21p:
                countElections['2021 Primary']+=1
            if voter.v22:
                countElections['2022 General']+=1
            if voter.v23:
                countElections['2023 Town']+=1
        # create the graph as Bar chart
        xElections = elections
        yElections = [countElections[election] for election in xElections]
        # generate the Bar chart
        fig = go.Bar(x=xElections, y=yElections)
        titleElection = "Voter Distribution by Previous Elections Voted"
        # obtain the graph as an HTML div"
        graph_div_elections = plotly.offline.plot(
            {"data": [fig], "layout_title_text": titleElection},
            auto_open=False,
            output_type="div"
        )
        # send div as template context variable
        context['graph_div_elections'] = graph_div_elections

        # count sample size
        nElections = sum(1 for v in voters if v.v20 or v.v21t or v.v21p or v.v22 or v.v23)
        # send nElections as template context variable
        context['nElections'] = nElections
#########                      END                            #########
        return context