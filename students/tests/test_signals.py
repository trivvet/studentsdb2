import logging
from StringIO import StringIO

from django.test import TestCase, override_settings

from students.models import Student, Group

@override_settings(LANGUAGE_CODE='en')

class SignalsTest(TestCase):
    
    def test_update_student(self):
        out = StringIO()
        handler = logging.StreamHandler(out)
        logging.root.addHandler(handler)
        group = Group(title='DemoGroup')
        group.save()
        
        student = Student(first_name='Demo', last_name="Student",
            ticket='1', birthday='1980-01-01', student_group=group)
        student.save()

        out.seek(0)
        self.assertEqual(out.readlines()[-1], 'Student added: Demo Student (ID: 1)\n')

        student.ticket = 5
        student.save()

        out.seek(0)
        self.assertEqual(out.readlines()[-1], 'Student updated: Demo Student (ID: 1)\n')

        logging.root.removeHandler(handler)

        

        

        
