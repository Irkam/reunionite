'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''

from django.db import models
from django.db.models import Model
from django.contrib.auth.models import Group, User
    

class Meeting(Model):
    name = models.CharField(max_length=64, blank=False)
    description = models.TextField(blank=False)
    location = models.CharField(max_length=64, blank=False)
    date_created = models.DateTimeField()
    date_closed = models.DateTimeField()
    restrict_group = models.ForeignKey(Group, blank=True, null=True)
    owner = models.ForeignKey(User)
    max_answers = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    def get_meeting(self):
        return {'meeting': self, 'dates': self.get_dates()}
    
    def get_results(self):
        return {'meeting': self, 'dates': [{'date': date, 'results': date.get_results()} for date in self.get_dates()]}
    
    def user_can_vote(self, user):
        return (user.groups.filter(name=self.restrict_group.name).exists() if self.restrict_group != None else True) or user.is_staff
    

class Date(Model):
    meeting = models.ForeignKey(Meeting)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def __str__(self):
        return str(self.start) + ">>" + str(self.end)
    
    def get_results_detailed(self):
        return [(choice, choice.get_answer_stats()) for choice in self.get_choices()]
    
    def get_results(self):
        return [{'choice': choice, 'result': len(choice.get_answers())} for choice in self.get_choices()]


class Availability(Model):
    meeting = models.ForeignKey(Meeting)
    date = models.ForeignKey(Date)
    user = models.ForeignKey(User)
    
    class Meta:
        order_with_respect_to = 'date'
        unique_together = ('meeting', 'date', 'user')        
    
    def __str__(self):
        return str(self.user) + "@" + str(self.date.start) + ">>" + str(self.date.end)



def get_dates(self):
    return Date.objects.all().filter(meeting=self)

def delete_availabilities(self, user):
    for d in Date.objects.all().filter(meeting=self):
        for answer in Availability.objects.all().filter(date=d):
            answer.delete()

Meeting.get_dates = get_dates
Meeting.delete_availabilities = delete_availabilities


def get_availabilities(self):
    return Availability.objects.all().filter(choice=self)

Date.get_availabilities = get_availabilities