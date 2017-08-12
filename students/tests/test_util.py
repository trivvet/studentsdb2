from django.test import TestCase
from django.http import HttpRequest

from students.util import get_current_group, get_groups, paginate
from students.models import Group, Student

class UtilsTestCase(TestCase):

    fixtures = ['demo_data3.json']

    def setUp(self):
        self.group = Group.objects.all()[1]

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
        
    def test_get_groups(self):

        # prepare our clean request
        request = HttpRequest()

        # add to request current group
        request.COOKIES['current_group'] = str(self.group.id)

        # check if we get corect list
        self.assertEqual(len(get_groups(request)), 3)
        self.assertEqual(get_groups(request)[1]['title'], self.group.title)
        self.assertEqual(get_groups(request)[1]['selected'], True)

    def test_paginate(self):

        # prepare list of students for function
        objects = Student.objects.all()

        # prepare our clean request
        request = HttpRequest()

        # test with clean page attribute
        paginate1 = paginate(objects, 3, request, {})
        self.assertEqual(len(paginate1['page_obj']), 3)
        self.assertEqual(paginate1['page_obj'].number, 1)
        
        # test with page attribute 999
        request = HttpRequest()
        request.GET.__setitem__('page', '999')
        paginate1 = paginate(objects, 3, request, {})
        self.assertEqual(len(paginate1['page_obj']), 2)
        self.assertEqual(paginate1['page_obj'].number, 2)

        # test with page attribute not integer
        request = HttpRequest()
        request.GET.__setitem__('page', 'robusta')
        paginate1 = paginate(objects, 3, request, {})
        self.assertEqual(len(paginate1['page_obj']), 3)
        self.assertEqual(paginate1['page_obj'].number, 1)

        # test with page attribute 2
        request = HttpRequest()
        request.GET.__setitem__('page', '2')
        paginate1 = paginate(objects, 3, request, {})
        self.assertEqual(len(paginate1['page_obj']), 2)
        self.assertEqual(paginate1['page_obj'].number, 2)
