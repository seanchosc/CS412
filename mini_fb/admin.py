## Register the models with the Django Admin tool
# mini_fb/admin.py
from django.contrib import admin


### Register your models here ###
from .models import Profile # import Profile model
admin.site.register(Profile) # register Profile 

from.models import StatusMessage # import StatusMessage model
admin.site.register(StatusMessage) # register StatusMessage