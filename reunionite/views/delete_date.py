'''
Created on 18 janv. 2015

@author: Mana
'''

from django.views.generic.base import View
from django.shortcuts import render
from django.http.response import Http404
from reunionite.models import *
from reunionite import forms
from django.core.exceptions import SuspiciousOperation, ValidationError


class DeleteDateView(View):
    template_name = "delete_date.html"
    
    def get(self, request, *args, **kwargs):
        try:
            date_form = forms.DateForm(initial={})
            return render(request, self.template_name, {'date_form': date_form,
                                                        'meeting_id': self.kwargs['meeting_id']})
        
        except Date.DoesNotExist:
            raise Http404
    
    
    def post(self, request, *args, **kwargs):
        date = Date()
        
        return date.remove()