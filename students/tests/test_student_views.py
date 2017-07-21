from datetime import datetime
import sys  

from django.test import TestCase, Client, override_settings
from django.urls import reverse

from students.models import Student, Group
reload(sys)  
sys.setdefaultencoding('utf8')

@override_settings(LANGUAGE_CODE='en')

class StudentsListViewTest(TestCase):

    fixtures = ['demo_data3.json']
    
    def setUp(self):

        self.client = Client()
        self.url = reverse('home')

    def test_student_list(self):
        self.client.login(username='trivvet2', password='Futycndj18')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertIn('Student1', response.content)
        #import pdb;pdb.set_trace()

        self.assertIn(reverse('students_edit',
            kwargs={'pk': Student.objects.filter(first_name='Student1')[0].id}),
            response.content)

        
        self.assertEqual(len(response.context['context']['students']), 3)

    def test_order_by(self):
        response = self.client.get(self.url, {'order_by': 'last_name'})

        self.assertEqual(response.status_code, 200)

        # test students list order
        self.assertEqual(response.context['context']['students'][0].last_name, 'LastName1')
        self.assertEqual(response.context['context']['students'][1].last_name, 'LastName2')
        self.assertEqual(response.context['context']['students'][2].last_name, 'LastName3')

        response = self.client.get(self.url, {'order_by': 'last_name', 'reverse': 1})

        self.assertEqual(response.status_code, 200)

        # test students list order
        self.assertEqual(response.context['context']['students'][0].last_name, 'LastName5')
        self.assertEqual(response.context['context']['students'][1].last_name, 'LastName4')
        self.assertEqual(response.context['context']['students'][2].last_name, 'LastName3')
