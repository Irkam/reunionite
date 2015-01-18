'''
Created on 18 janv. 2015

@author: jivay
'''
from django.views.generic.base import View
from django.shortcuts import render
from django.http.response import Http404
from reunionite.models import *
from reunionite import forms
from django.core.exceptions import SuspiciousOperation, ValidationError


class DateView(View):
    template_name = "date.html"
    
    def get(self, request, *args, **kwargs):
        try:
            date = Date.objects.get(pk=self.kwargs['date_id'])
            date_form = forms.DateForm(initial={'start': date.start, 'end': date.end,})
            return render(request, self.template_name, {'date': date,
                                                        'date_form': date_form,
                                                        'date_id': date.id,
                                                        'meeting_id': self.kwargs['meeting_id']})
        
        except Date.DoesNotExist:
            raise Http404
    
    def post(self, request, *args, **kwargs):
        try:
            date = Date.objects.get(pk=self.kwargs['date_id'])
                
                
            date_form = forms.DateForm(request.POST)
            
            if not date_form.is_valid():
                raise ValidationError('invalid date')
            
            date.meeting = Meeting.objects.get(pk=self.kwargs['meeting_id'])
            date.start = request.POST['start']
            date.end = request.POST['end']
            date.save() 
            
            return render(request, self.template_name, {'date': date,
                                                        'date_form': date_form,
                                                        'date_id': date.id,
                                                        'meeting_id': self.kwargs['meeting_id']})
        
        except Date.DoesNotExist:
            raise SuspiciousOperation  