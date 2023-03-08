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
        #print('run setup')
        self.client = APIClient()
        self.user = self.createUser(
            username= 'test_user',
            email= 'test@gmail.com',
            password= 'testtest'
        )

    def createUser(self, username, email, password):
        return User.objects.create_user(username, email, password)

    def test_login(self):
        # use GET instead of POST, should return 405
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'testtest',
        })
        # check status, 405 means methods not allowed
        self.assertEqual(response.status_code, 405)

        # now use POST, but wrong password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong',
        })
        # check status
        self.assertEqual(response.status_code, 400)

        # check log in status, should be False
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)
        # check correct login
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'testtest',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], 'test@gmail.com')

        # check log in status, should be True now
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logout(self):
        # log in first
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'testtest',
        })
        # check log in status, should be True now
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        # use GET instead of POST, should return 405
        response = self.client.get(LOGOUT_URL)
        # check status, 405 means methods not allowed
        self.assertEqual(response.status_code, 405)

        # run POST, should return 200
        response = self.client.post(LOGOUT_URL)
        # check status should be 200
        self.assertEqual(response.status_code, 200)

        # check log in status, should be False now
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@gmail.com',
            'password': 'somepassword',
        }
        # test using GET instead of POST
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # test wrong email
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not correct email',
            'password': 'somepassword',
        })
        #print(response.data)
        self.assertEqual(response.status_code, 400)

        # test too short password
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not correct email',
            'password': 's',
        })
        self.assertEqual(response.status_code, 400)

        # test too long username
        response = self.client.post(SIGNUP_URL, {
            'username': 'someoneeeeeeeeeeeee',
            'email': 'someone@gmail.com',
            'password': 'somepassword',
        })
        self.assertEqual(response.status_code, 400)

        # test correct sign up
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'someone')
        # check log in status
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)
