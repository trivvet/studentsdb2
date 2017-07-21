import StringIO

from django.test import TestCase, override_settings
from django.core.management import call_command

@override_settings(LANGUAGE_CODE='en')

class CommandTest(TestCase):
    fixtures = ['demo_data3.json']

    def test_command(self):
        out = StringIO.StringIO()
        call_command('stcount', 'student', 'group', 'user', stdout=out)

        result = out.getvalue()
        self.assertIn('Number of students in database: 5', result)
        self.assertIn('Number of groups in database: 3', result)
        self.assertIn('Number of users in database: 1', result)
