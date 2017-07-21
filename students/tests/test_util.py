from django.test import TestCase
from django.http import HttpRequest

from students.util import get_current_group
from students.models import Group

class UtilTests(TestCase):
	
    def setUp(self):
        group, created = Group.objects.get_or_create(title='BM')
        self.group = group	
	
    def test_get_current_group(self):
		
        request = HttpRequest()
		
		# check with no cookie set
        self.assertEqual(get_current_group(request), None)
		
		# check with invalid cookie
        request.COOKIES['current_group'] = '12345'
        self.assertEqual(get_current_group(request), None)
		
        # check with valid cookie
        request.COOKIES['current_group'] = str(self.group.id)
        self.assertEqual(get_current_group(request), self.group)
