'''
Created on 18 janv. 2015

@author: Mana
'''

from django.shortcuts import render
from django.views.generic import View
from django.http import Http404
from django.contrib.auth.models import User
from reunionite.models import *
from reunionite.forms import RegisterUserForm
from django.core.exceptions import ValidationError

class LogoutView(View):
    template_name = "registration/logout.html"
    
    def get(self, request, *args, **kwargs):
        """TODO"""
        
    def post(self, request, *args, **kwargs):
        """TODO"""