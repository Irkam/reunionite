'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''
from django.shortcuts import render
from django.views.generic import View
from django.db import transaction
from django.http import Http404
from reunionite.models import *
from reunionite.forms import MeetingForm
from django.core.exceptions import SuspiciousOperation, PermissionDenied, ValidationError
import re

import pdb
from itertools import groupby

class MeetingView(View):
    template_name = "meeting.html"
    regex = re.compile("^q(\d+)$")
    
    def get(self, request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(pk=self.kwargs['meeting_id'])
            
            if meeting.user_can_vote(request.user):
                meeting_form = MeetingForm(meeting)()
                """
                dates = meeting.get_meeting()['dates']
                dates_ordered = []
                for year, dates_years in groupby(dates, lambda x:x['keys'][0]):
                    for month, dates_months in groupby(dates_years, lambda x:x['keys'][1]):
                        for day, dates_days in groupby(dates_months, lambda x:x['keys'][2]):
                            for hour, dates_hours in groupby(dates_days, lambda x:x['keys'][3]):
                                pdb.set_trace()
                                pass
                """
                
                return render(request, self.template_name, {'meeting': meeting.get_meeting(),
                                                            'meeting_form': meeting_form,})
            else:
                raise PermissionDenied
            
        except Meeting.DoesNotExist:
            raise Http404
    
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:            
            meeting = Meeting.objects.get(pk=self.kwargs['meeting_id'])
            meeting_form = MeetingForm(meeting)(request.POST)
            
            if not meeting_form.is_valid():
                raise ValidationError("invalid form")
            
            if not meeting.user_can_vote(request.user) or request.user.is_anonymous():
                raise PermissionDenied
            
            meeting.delete_availabilities(request.user)
            
            if meeting.user_can_vote(request.user):
                if meeting.max_answers == 1:
                    date = meeting_form.cleaned_data['dates']
                    
                    availability = Availability()
                    availability.meeting = meeting
                    availability.date = date
                    availability.user = request.user
                    availability.save()
                
                else:
                    for date in meeting_form.cleaned_data['dates'] :                    
                        availability = Availability()
                        availability.meeting = meeting
                        availability.date = date
                        availability.user = request.user
                        availability.save()
                        
                return render(request, self.template_name, {'meeting': meeting.get_meeting(),
                                                            'meeting_form': meeting_form,
                                                            })
            else:
                raise PermissionDenied
        except Meeting.DoesNotExist:
            raise Http404