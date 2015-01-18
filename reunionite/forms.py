'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''

from django import forms
from django.forms import Form
from reunionite.models import *

class CreateMeetingForm(Form):
    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(max_length=64, required=True)
    location = forms.CharField(max_length=64, required=True)
    #date_closed = forms.DateTimeField()
    max_answers = forms.IntegerField()

class EditMeetingForm(Form):
    name = forms.CharField(max_length=64, required=True)
    description = forms.CharField(max_length=64, required=True)
    location = forms.CharField(max_length=64, required=True)
    #date_closed = forms.DateTimeField()

class DateForm(Form):
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    
class RegisterUserForm(Form):
    username = forms.CharField(max_length=32, required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

class EditUserForm(Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

def MeetingForm(meeting):
    """
        creates a form from a meeting
        useful for validation, not much for displaying
        
        :param meeting: a meeting
        :type meeting: reunionite.models.Meeting instance
    """
    qs = Date.objects.all().filter(meeting=meeting)
    w =  forms.RadioSelect if meeting.max_answers == 1 else forms.CheckboxSelectMultiple
    
    if meeting.max_answers == 1:
        dates_form = forms.ModelChoiceField(queryset=qs, widget=w, empty_label=None, required=True)
    else:
        dates_form = forms.ModelMultipleChoiceField(queryset=qs, widget=w, required=True)
    return type('PollForm', (Form, ), {'dates': dates_form})