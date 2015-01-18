'''
Created on 15 janv. 2015

@author: Mana
'''
from django.shortcuts import render
from django.views.generic import View
from reunionite.models import *

class MeetingsView(View):
    """
        TODO: ajouter filtre restriction
    """
    template_name = "meetings.html"
    
    def get(self, request, *args, **kwargs):
        offset = self.request.GET.get('meetings_offset', 0)
        meetings = Meeting.objects.all()[offset:offset+25]
        return render(request, self.template_name, {'meetings': meetings,})