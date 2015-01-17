'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''

from django.db import models
from django.db.models import Model
from django.contrib.auth.models import Group, User
from django.core import urlresolvers
from django.core.exceptions import ValidationError
    

class Meeting(Model):
    name = models.CharField(max_length=64, blank=False)
    description = models.TextField()
    date_created = models.DateTimeField()
    date_closed = models.DateTimeField()
    restrict_group = models.ForeignKey(Group, blank=True, null=True)
    owner = models.ForeignKey(User)
    
    def __str__(self):
        return self.name
    
    def get_poll(self):
        return {'poll': self, 'questions': [{'question': question, 'choices': question.get_choices()} for question in self.get_questions()]}
    
    def get_results(self):
        return {'poll': self, 'questions': [{'question': question, 'results': question.get_results()} for question in self.get_questions()]}
    
    def user_can_vote(self, user):
        return (user.groups.filter(name=self.restrict_group.name).exists() if self.restrict_group != None else True) or user.is_staff
    

class Date(Model):
    meeting = models.ForeignKey(Meeting)
    datetime = models.DateTimeField()
    
    def __str__(self):
        return self.datetime
    
    def edit_link(self):
        if self.id:
            url = urlresolvers.reverse('admin:PollPy_question_change', args=(self.id, ))
            return '<a href="%s" target="_popup">Details</a>' % url
        return 'You need to save before adding choices'
    edit_link.allow_tags = True
    edit_link.short_description = ''
    
    def get_results_detailed(self):
        return [(choice, choice.get_answer_stats()) for choice in self.get_choices()]
    
    def get_results(self):
        return [{'choice': choice, 'result': len(choice.get_answers())} for choice in self.get_choices()]


class Availability(Model):
    date = models.ForeignKey(Date)
    user = models.ForeignKey(User)
    
    class Meta:
        order_with_respect_to = 'choice'
        unique_together = ('question', 'choice', 'user')        
    
    def __str__(self):
        if self.choice.is_text:
            return self.content
        else:
            return (str(self.question) + " "  + str(self.choice))



def get_dates(self):
    return Date.objects.all().filter(meeting=self)

def delete_availabilities(self, user):
    for d in Date.objects.all().filter(meeting=self):
        for answer in Availability.objects.all().filter(date=d):
            answer.delete()

Meeting.get_questions = get_dates
Meeting.delete_answers = delete_availabilities


def get_availabilities(self):
    return Availability.objects.all().filter(choice=self)

Date.get_availabilities = get_availabilities