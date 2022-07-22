from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login_call')
        self.user={
            'email': 'testemail@gmail.com',
            'password': 'password',
            'passwordrepeat': 'passwordrepeat',
        }
        self.user_short_password={
            'email': 'testemail@gmail.com',
            'password': 'tes',
            'passwordrepeat': 'tes'
        }
        self.user_notmatching_password={
            'email': 'testemail@gmail.com',
            'password': 'tes123',
            'passwordrepeat': 'tes345'
        }
        self.user_invalid_email={
            'email': 'test.com',
            'password': 'tes123',
            'passwordrepeat': 'tes123'
        }
        return super().setUp()

class RegisterTest(BaseTest):
    def test_view_page_correctly(self):
        response=self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'register.html')

    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

    def test_cant_register_user_withshortpassword(self):
        response=self.client.post(self.register_url,self.user_short_password,format='text/html')
        self.assertEqual(response.status_code,302)
    
    def test_cant_register_user_with_notmatching_passwords(self):
        response=self.client.post(self.register_url,self.user_notmatching_password,format='text/html')
        self.assertEqual(response.status_code,302)
    
    def test_cant_register_user_with_invalid_email(self):
        response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
        self.assertEqual(response.status_code,302)

    def test_cant_register_user_with_existing_email(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

    
class LoginTest(BaseTest):
    def test_can_access_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'login.html')
    

