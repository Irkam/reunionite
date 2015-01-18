'''
Created on 31 déc. 2014

@author: Jean-Vincent
'''
from django.shortcuts import render
from django.views.generic import View
from django.http import Http404
from reunionite.models import *
from django.core.exceptions import PermissionDenied

class MeetingResultsView(View):
    template_name = "results.html"
    
    def get(self, request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(pk=request.GET.get('poll_id'))
            
            if meeting.owner == request.user:
                return render(request, self.template_name, {'results': meeting.get_results()})
            else:
                raise PermissionDenied
            
        except Meeting.DoesNotExist:
            raise Http404