'''
Created on 15 janv. 2015

@author: Mana
'''
from django.shortcuts import render
from django.views.generic import View
from PollPy.models import *

class PollsView(View):
    """
        TODO: ajouter filtre restriction
    """
    template_name = "polls.html"
    
    def get(self, request, *args, **kwargs):
        offset = self.request.GET.get('polls_offset', 0)
        polls = Poll.objects.all()[offset:offset+25]
        return render(request, self.template_name, {'polls': polls,})