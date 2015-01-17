'''
Created on 15 janv. 2015

@author: Mana
'''
'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''
from django.shortcuts import render
from django.views.generic import View

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {})