'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''
from django.shortcuts import render
from django.views.generic import View
from django.db.utils import IntegrityError
from django.db import transaction
from django.http import Http404
from reunionite.models import *
from reunionite.forms import MeetingForm
from django.core.exceptions import SuspiciousOperation, PermissionDenied, ValidationError
import re

class MeetingView(View):
    template_name = "poll.html"
    regex = re.compile("^q(\d+)$")
    
    def get(self, request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(pk=self.kwargs['meeting_id'])
            
            if meeting.user_can_vote(request.user):
                return render(request, self.template_name, {'meeting': meeting.get_meeting(),
                                                            })
            else:
                raise PermissionDenied
            
        except Meeting.DoesNotExist:
            raise Http404
    
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(pk=self.kwargs['poll_id'])
            meeting_form = MeetingForm(meeting)(request.POST)
            
            if not meeting_form.is_valid():
                raise ValidationError("invalid form")
            
            if not meeting.user_can_vote(request.user):
                raise PermissionDenied
            
            meeting.delete_answers(request.user)
            
            if meeting.user_can_vote(request.user):
                for q, c in request.POST.lists():
                    regmatch = self.regex.match(q)
                    if regmatch:
                        try:
                            question = Question.objects.get(pk=regmatch.group(1))
                            if question.poll != meeting:
                                raise SuspiciousOperation
                            
                            for c_id in c:
                                try:
                                    choice = Choice.objects.get(pk=c_id)
                                    if choice.question == question:
                                        answer = Answer()
                                        answer.user = request.user
                                        answer.question = question
                                        answer.choice = choice
                                        answer.content = request.POST.get(q+'_c'+c[0], '') if choice.is_text else ''
                                        try:
                                            answer.save()
                                        except ValidationError as ve:
                                            raise ve
                                    else:
                                        raise SuspiciousOperation
                                    
                                except Choice.DoesNotExist:
                                    raise SuspiciousOperation
                                
                                except IntegrityError:
                                    #TODO: renvoyer autre-chose qui indique qu'on essaye de gruger
                                    raise SuspiciousOperation
                            
                            
                            if (question.required == True and
                                Answer.objects.all().filter(question=question, user=request.user).count() == 0):
                                raise ValidationError('Did not answer required question')
                        
                        except Question.DoesNotExist:
                            raise SuspiciousOperation
                        
                return render(request, self.template_name, {'meeting': meeting.get_poll(),
                                                            })
            else:
                raise PermissionDenied
        except Meeting.DoesNotExist:
            raise Http404