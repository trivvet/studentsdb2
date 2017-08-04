from django.core import mail
from django.test import TestCase, override_settings, Client
from django.urls import reverse

@override_settings(LANGUAGE_CODE='en')

class ContactAdminFormTests(TestCase):
    fixtures = ['demo_data3.json']

    def test_send_email(self):
        # prepare client and login as administrator
        client = Client()
        client.login(username='trivvet2', password='Futycndj18')

        # make form submit
        response = client.post(reverse('contact_admin'),
            {'from_email': 'test@gmail.com',
            'subject': 'Test Email',
            'message': 'Test Email Body'}, follow=True)

        # check if test email backend catched our email to admin
        message = mail.outbox[0]
        self.assertEqual(message.body, 'Test Email Body')
        self.assertEqual(message.from_email, 'test@gmail.com')
        self.assertEqual(message.subject, 'Test Email')

        # ckeck if we have right redirect
        self.assertEqual(response.status_code, 200)
        self.assertIn('Letter send successfully', response.content)
        
    
