from django.test import TestCase
from .models import User
from django.contrib import auth

# Create your tests here.

class AuthTestCase(TestCase):
    def setUp(self):
        print("######################")
        self.u = User.objects.create_user(username = 'pera', email='pera@gmail.com', password = '123')
        self.u.is_staff = True
        self.u.is_superuser = True
        self.u.is_active = True
        self.u.save()

    def testLogin(self):
        print("######### LOGIN")
        self.client.login(username='pera', password='123')
        print("*********************")
        print(self.client.login(username='test', password='123'))
