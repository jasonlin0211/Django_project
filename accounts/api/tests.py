from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

LOGIN_URL = 'api/accounts/login/'
LOGOUT_URL = 'api/accounts/logout/'
SIGNUP_URL = 'api/accounts/signup/'
LOGIN_STATUS_URL = 'api/accounts/login_status/'
# Create your tests here.

class AccountApiTests(TestCase):

    def setUp(self):
        # this function will be executed when every test case is executed
        self.client = APIClient
        self.user = self.createUser(
            username= 'test_user',
            email= 'test@gmail.com',
            password= 'testtest'
        )

    def createUser(self, username, email, password):
        return User.objects.create_user(username, email, password)

