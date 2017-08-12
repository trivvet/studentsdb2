from django.test import TestCase
from django.http import HttpRequest
from django.template import Template, Context

from students.models import Student
from students.util import paginate

class TemplateTagsTest(TestCase):

    fixtures = ['demo_data3.json']

    def test_str2int(self):
        out = Template(
        "{% load str2int %}"
        "{% if 10 == '10'|str2int %}"
        "done"
        "{% endif %}").render(Context({}))
        
        self.assertIn('done', out)

    def test_pagenav(self):
        # prepare list of students for function
        objects = Student.objects.all()

        # prepare our clean request
        request = HttpRequest()

        # prepare data for templatetag
        paginate_data = paginate(objects, 3, request, {})

        out = Template(
            "{% load pagenav %}"
            "{% pagenav context.page_obj context.is_paginated context.paginator %}"
            ).render(Context({'context': paginate_data}))

        # check our tag for obvious content
        self.assertIn('<!-- Pagination -->', out)
        self.assertIn('>1</a>\n', out)
        self.assertIn('<nav aria-label="Page navigation">', out)
        self.assertIn('<span aria-hidden="true">&raquo;</span>', out)
