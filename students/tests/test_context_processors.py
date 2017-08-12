from django.test import TestCase
from django.http import HttpRequest
from django.template import Template, Context

from students.context_processors import groups_processor

class ContextProcessorsTest(TestCase):

    fixtures = ['demo_data3.json']
    
    def test_context_processors(self):
        request = HttpRequest()
        groups = groups_processor(request)['groups_all']

        #import pdb;pdb.set_trace()
        
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups[0]['title'], 'Group1')
        self.assertEqual(groups[2]['title'], 'Group3')
