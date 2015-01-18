'''
Created on 31 déc. 2014

@author: Jean-Vincent
'''
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from reunionite import forms
from reunionite.models import Meeting
from datetime import datetime

class CreateMeetingView(View):
    template_name = "create.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateMeetingView, self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        create_form = forms.CreateMeetingForm()
        return render(request, self.template_name, {'create_form': create_form})
    
    def post(self, request, *args, **kwargs):
        create_form = forms.CreateMeetingForm(request.POST)
        
        if not create_form.is_valid():
            raise ValidationError('invalid meeting')
        
        values = create_form.cleaned_data
        meeting = Meeting()
        meeting.name = values['name']
        meeting.description = values['description']
        meeting.location = values['location']
        meeting.date_created = datetime.today()
        meeting.date_closed = datetime.today()
        meeting.restrict_group = None
        meeting.owner = request.user
        meeting.max_answers = values['max_answers']
        meeting.save()
        
        return redirect('edit', meeting.id)