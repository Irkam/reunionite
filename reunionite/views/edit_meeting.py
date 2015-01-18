'''
Created on 17 janv. 2015

@author: Jean-Vincent
'''
from django.views.generic import View
from reunionite.models import Meeting
from django.core.exceptions import PermissionDenied, ValidationError
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
            
            meeting_form = EditMeetingForm(initial={'name': meeting.name, 'description': meeting.description, 'location': meeting.location, 'date_closed': meeting.date_closed})
            return render(request, self.template_name, {'meeting': meeting.get_meeting(),
                                                        'meeting_form': meeting_form,})
        
        except Meeting.DoesNotExist:
            raise Http404
    
    def post(self, request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(pk=self.kwargs['meeting_id'])
            
            if meeting.owner != request.user:
                raise PermissionDenied
            
            meeting_form = EditMeetingForm(request.POST)
            if not meeting_form.is_valid():
                raise ValidationError('invalid modification')
            
            values = meeting_form.cleaned_data
            meeting.name = values['name']
            meeting.description = values['description']
            meeting.location = values['location']
            meeting.date_closed = values['date_closed']
            meeting.restrict_group = None
            meeting.owner = request.user
            meeting.max_answers = values['max_answers']
            meeting.save()
            
            return render(request, self.template_name, {'meeting': meeting.get_meeting(),
                                                        'meeting_form': meeting_form,})
        
        except Meeting.DoesNotExist:
            raise Http404