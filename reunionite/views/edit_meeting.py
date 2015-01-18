'''
Created on 17 janv. 2015

@author: Jean-Vincent
'''
from django.views.generic import View
from reunionite.models import Meeting
from django.core.exceptions import PermissionDenied
from reunionite.forms import MeetingForm, EditMeetingForm
from django.shortcuts import render
from django.http.response import Http404

class EditMeetingView(View):
    template_name = "edit.html"
    
    def get(self, request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(pk=self.kwargs['meeting_id'])
            
            if meeting.owner != request.user:
                raise PermissionDenied
            
            meeting_form = EditMeetingForm()
            return render(request, self.template_name, {'meeting': meeting.get_meeting(),
                                                        'meeting_form': meeting_form,})
        
        except Meeting.DoesNotExist:
            raise Http404
    
    def post(self, request, *args, **kwargs):
        pass