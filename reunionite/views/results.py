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
            poll = Poll.objects.get(pk=self.kwargs['poll_id'])
            
            if poll.owner == request.user:
                return render(request, self.template_name, {'poll_name': poll.name,
                                                            'results': poll.get_results(),
                                                            })
            else:
                raise PermissionDenied
            
        except Poll.DoesNotExist:
            raise Http404