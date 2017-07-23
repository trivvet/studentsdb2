from django.test import TestCase, Client, override_settings
from django.urls import reverse

from students.models import Student, Group

@override_settings(LANGUAGE_CODE='en')

class StudentsUpdateFormTest(TestCase):

    fixtures = ['demo_data3.json']
    
    def setUp(self):

        # remember url to edit form
        self.url = reverse('students_edit', kwargs={'pk': '1'})

        # remember test browser
        self.client = Client()

    def test_form_get(self):

        # login admin user, make request to the server and check answer
        self.client.login(username='trivvet2', password='Futycndj18')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # check obvious content
        self.assertIn(u'Editing student', response.content)
        self.assertIn(u'Ticket', response.content)
        self.assertIn(u'Last Name', response.content)
        self.assertIn(u'name="save_button"', response.content)
        self.assertIn(u'name="cancel_button"', response.content)
        self.assertIn(u'First Name', response.content)

    def test_success(self):

        # login admin user, make post request to the server and check answer
        self.client.login(username='trivvet2', password='Futycndj18')
        response = self.client.post(self.url, {'first_name': 'Student1 Updated',
            'ticket': 11, 'last_name': 'LastName1 Updated',
            'birthday': '1987-01-01', 'student_group': 2}, follow=True)
        self.assertEqual(response.status_code, 200)

        # test updated student data
        student = Student.objects.get(pk=1)
        self.assertEqual(student.first_name, 'Student1 Updated')
        self.assertEqual(student.last_name, 'LastName1 Updated')
        self.assertEqual(student.ticket, 11)
        self.assertEqual(student.student_group.id, 2)

        # test response from server
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertIn('saved successfully!', response.content)

    def test_access(self):
        response = self.client.get(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Login Form', response.content)

        self.assertEqual(response.redirect_chain[0], ('/users/login/?next=/students/1/edit/', 302))
        
