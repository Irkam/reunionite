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

def PollForm(poll):
    """
        creates a form from a poll
        useful for validation.
        
        :param poll: a poll
        :type poll: reunionite.models.Poll instance
    """
    fields = dict()
    for question in Question.objects.all().filter(poll=poll):
        qs = Choice.objects.all().filter(question=question)
        
        fields['q'+str(question.id)] = forms.ModelChoiceField(queryset=qs, required=question.required)
        for textchoice in qs.filter(is_text=True):
            fields['q'+str(question.id)+'_c'+str(textchoice.id)] = forms.CharField(max_length=32, required=True if qs.count()==1 and question.required==True else False)
    
    return type('PollForm', (Form, ), fields)