'''
Created on 26 déc. 2014

@author: Jean-Vincent
'''
from django.test import TestCase
from PollPy.models import Poll


class PollTest(TestCase):
    def setUp(self):
        Poll(title="toast")

    def testPoll(self):
        pass