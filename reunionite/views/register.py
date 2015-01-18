'''
Created on 31 déc. 2014

@author: Jean-Vincent
'''
from django.shortcuts import render
from django.views.generic import View
from django.http import Http404
from django.contrib.auth.models import User
from reunionite.models import *
from reunionite.forms import RegisterUserForm
from django.core.exceptions import ValidationError

class RegisterView(View):
    template_name = "registration/register.html"
    
    def get(self, request, *args, **kwargs):
        register_form = RegisterUserForm()
        try:
            return render(request, self.template_name, {'register_form': register_form,})
        except Poll.DoesNotExist:
            raise Http404
    
    def post(self, request, *args, **kwargs):
        """Attempts to register a new user using POST data
        TODO
        This needs to be secure
        """
        register_form = RegisterUserForm(data=request.POST)
        if register_form.is_valid():
            if request.POST.get('password') != request.POST.get('password_confirm'):
                raise ValidationError("Password doesn't match")
            
            new_user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
            #TODO : login the user
                    
            return render(request, "home.html", {})
        else:
            raise ValidationError