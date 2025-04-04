# voter_analytics/views.py
#
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Voter # import the voter mdel

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
        return voters