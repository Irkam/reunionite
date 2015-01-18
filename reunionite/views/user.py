'''
Created on 17 janv. 2015

@author: Jean-Vincent
'''
from django.shortcuts import render
from django.views.generic import View
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth.models import *
from django.http.response import Http404
from reunionite.models import *
from reunionite.forms import EditUserForm

class UserView(View):
    template_name = "user.html"
    
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=request.POST.get('uid')) if request.POST.get('uid', None) != None else request.user
            meetings = Meeting.objects.all().filter(owner=user)
            edit_form = EditUserForm(initial={'email': user.email})
            return render(request, self.template_name, {'this_user': user,
                                                        'meetings': meetings,
                                                        'user_edit_form': edit_form,})
        
        except User.DoesNotExist:
            raise Http404
    
    def post(self, request, *args, **kwargs):
        pass