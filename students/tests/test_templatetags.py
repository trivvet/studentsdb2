from django.test import TestCase
from django.template import Template, Context

class TemplateTagsTest(TestCase):

    def test_str2int(self):
        out = Template(
        "{% load str2int %}"
        "{% if 10 == '10'|str2int %}"
        "done"
        "{% endif %}").render(Context({}))
        
        self.assertIn('done', out)
