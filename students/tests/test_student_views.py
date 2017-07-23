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

        # remember test browser
        self.client = Client()

        # remember url to our homepage
        self.url = reverse('home')

    def test_student_list(self):

        # login admin user
        self.client.login(username='trivvet2', password='Futycndj18')

        # make request to the server to get homepage
        response = self.client.get(self.url)

        # check status from the server
        self.assertEqual(response.status_code, 200)

        # check if we have student name on a page
        self.assertIn('Student1', response.content)

        # check link for student edit form
        self.assertIn(reverse('students_edit',
            kwargs={'pk': Student.objects.filter(first_name='Student1')[0].id}),
            response.content)

        # ensure that we have 3 students on the page
        self.assertEqual(len(response.context['context']['students']), 3)

    def test_current_group(self):

        # set group1 as currently selected group
        group = Group.objects.filter(title='Group2')[0]
        self.client.cookies['current_group'] = group.id

        # make request to the server to get homepage and check status
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # in group2 we have only 1 student
        self.assertEqual(len(response.context['context']['students']), 1)

    def test_order_by(self):
        response = self.client.get(self.url, {'order_by': 'last_name'})

        self.assertEqual(response.status_code, 200)

        # test students list order
        students = response.context['context']['students']
        self.assertEqual(students[0].last_name, 'LastName1')
        self.assertEqual(students[1].last_name, 'LastName2')
        self.assertEqual(students[2].last_name, 'LastName3')

        response = self.client.get(self.url, {'order_by': 'last_name', 'reverse': 1})

        self.assertEqual(response.status_code, 200)

        # test students list order
        students = response.context['context']['students']
        self.assertEqual(students[0].last_name, 'LastName5')
        self.assertEqual(students[1].last_name, 'LastName4')
        self.assertEqual(students[2].last_name, 'LastName3')
