'''
Created on 17 janv. 2015

@author: Jean-Vincent
'''
from django.views.generic import View

class EditPollView(View):
    template_name = "edit_poll.html"