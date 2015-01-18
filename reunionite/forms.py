'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''

from django import forms
from django.forms import Form
from reunionite.models import *
    
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
        useful for validation.
        
        :param meeting: a meeting
        :type meeting: reunionite.models.Meeting instance
    """
    return type('PollForm', (Form, ), {'dates': forms.MultipleChoiceField(queryset=Date.objects.all().filter(meeting=meeting), required=True)})