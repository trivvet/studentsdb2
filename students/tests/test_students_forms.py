import tempfile
import os

from PIL import Image

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist

from students.models import Student, Group

MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(LANGUAGE_CODE='en', MEDIA_ROOT=MEDIA_ROOT)

class StudentsUpdateFormTest(TestCase):

    fixtures = ['demo_data3.json']

    def _create_image(self):

        with tempfile.NamedTemporaryFile(prefix='text_file', suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')
 
        return open(f.name, mode='rb')
    
    def setUp(self):

        # remember url to edit form
        self.url = reverse('students_edit', kwargs={'pk': '1'})
        self.url_delete = reverse('students_delete', kwargs={'pk': '1'})

        # remember test browser
        self.client = Client()

        # remember test image
        self.image = self._create_image()

    def tearDown(self):
        os.remove(self.image.name)
        #import pdb;pdb.set_trace()
        try:
            os.remove(Student.objects.get(pk=1).photo.file.name)
        except:
            pass

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

        # check css styles
        self.assertIn('form-horizontal', response.content)
        self.assertIn('form-group', response.content)

    def test_cancel(self):
        self.client.login(username='trivvet2', password='Futycndj18')
        response = self.client.post(self.url, {'cancel_button': True}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Editing student canceled!', response.content)

    def test_success(self):

        # login admin user, make post request to the server and check answer
        self.client.login(username='trivvet2', password='Futycndj18')
        response = self.client.post(self.url, {'first_name': 'Student1 Updated',
            'ticket': 11, 'last_name': 'LastName1 Updated', 'photo': self.image,
            'birthday': '1987-01-01', 'student_group': 2}, follow=True)
        self.assertEqual(response.status_code, 200)

        # test updated student data
        student = Student.objects.get(pk=1)
        self.assertEqual(student.first_name, 'Student1 Updated')
        self.assertEqual(student.last_name, 'LastName1 Updated')
        self.assertEqual(student.ticket, 11)
        self.assertEqual(Image.open(student.photo), Image.open(self.image))
        self.assertEqual(student.student_group.id, 2)

        # test response from server
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertIn('saved successfully!', response.content)

    def test_access(self):
        response = self.client.get(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Login Form', response.content)

        self.assertEqual(response.redirect_chain[0], ('/users/login/?next=/students/1/edit/', 302))

    def test_delete_cancel(self):
        self.client.login(username='trivvet2', password='Futycndj18')
        response = self.client.post(self.url_delete, {'cancel_button': True}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Deleting student canceled', response.content)

    def test_delete_success(self):
        self.client.login(username='trivvet2', password='Futycndj18')
        response = self.client.post(self.url_delete, follow=True)

        self.assertEqual(response.status_code, 200)
        try:
            Student.objects.get(pk=1)
        except ObjectDoesNotExist:
            pass
        else:
            1/0

        # test response from server
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertIn('deleted successfully', response.content)

    def test_delete_access(self):
        response = self.client.get(self.url_delete, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Login Form', response.content)

        self.assertEqual(response.redirect_chain[0], ('/users/login/?next=/students/1/delete', 302))
        
