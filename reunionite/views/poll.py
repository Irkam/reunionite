'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''
from django.shortcuts import render
from django.views.generic import View
from django.db.utils import IntegrityError
from django.db import transaction
from django.http import Http404
from PollPy.models import *
from PollPy.forms import PollForm
from django.core.exceptions import SuspiciousOperation, PermissionDenied, ValidationError
import re

class PollView(View):
    template_name = "poll.html"
    regex = re.compile("^q(\d+)$")
    
    def get(self, request, *args, **kwargs):
        try:
            poll = Poll.objects.get(pk=self.kwargs['poll_id'])
            
            if poll.user_can_vote(request.user):
                return render(request, self.template_name, {'poll_name': poll.name,
                                                            'poll': poll.get_poll(),
                                                            })
            else:
                raise PermissionDenied
            
        except Poll.DoesNotExist:
            raise Http404
    
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            poll = Poll.objects.get(pk=self.kwargs['poll_id'])
            poll_form = PollForm(poll)(request.POST)
            
            if not poll_form.is_valid():
                raise ValidationError("invalid form")
            
            if not poll.user_can_vote(request.user):
                raise PermissionDenied
            
            poll.delete_answers(request.user)
            
            if poll.user_can_vote(request.user):
                for q, c in request.POST.lists():
                    regmatch = self.regex.match(q)
                    if regmatch:
                        try:
                            question = Question.objects.get(pk=regmatch.group(1))
                            if question.poll != poll:
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
                        
                return render(request, self.template_name, {'poll_name': poll.name,
                                                            'poll': poll.get_poll(),
                                                            })
            else:
                raise PermissionDenied
        except Poll.DoesNotExist:
            raise Http404