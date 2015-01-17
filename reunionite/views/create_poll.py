'''
Created on 31 déc. 2014

@author: Jean-Vincent
'''
from django.shortcuts import render
from django.views.generic import View
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from reunionite.models import *

class CreatePollView(View):
    template_name = "create.html"
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreatePollView, self).dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name, {})
        except Poll.DoesNotExist:
            raise Http404