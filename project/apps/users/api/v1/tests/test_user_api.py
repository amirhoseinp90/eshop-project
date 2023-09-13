"""
Tests for users APIs.
"""
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from project.apps.users.models import User
from project.apps.users.api.v1.serializers import CreateUserSerializer


CREATE_USER_URL = reverse('v1:create-user')
CREATE_TOKEN_URL = reverse('v1:create-token')


def create_user(username='testusername', email='test@example.com', password='test123', **params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(username, email, password, **params)


class PublicUserApiTests(TestCase):
    """Test unauthenticated API requests."""
    client_class = APIClient

    def test_register_user_successfull(self):
        """Test creating a user is successful"""
        payload = {
            'username': 'testusername',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test creating a user returns error if user with email exists."""
        payload = {
            'username': 'newusername',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        create_user(email=payload['email'])
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_username_exists_error(self):
        """Test creating a user returns error if user with username exists."""
        payload = {
            'username': 'testusername',
            'email': 'newemail@example.com',
            'password': 'testpass123'
        }
        create_user(username=payload['username'])
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error returned if user password is less than 5 chars."""
        payload = {
            'username': 'testusername',
            'email': 'test@example.com',
            'password': 'pass'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        is_user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(is_user_exists)

    def test_create_token_for_user_successful(self):
        """Test generating token for valid credentials is successful."""
        user_details = {
            'username': 'testusername',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_user_does_not_exists(self):
        """Test an error returned if user does not exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_bad_credentials_error(self):
        """Test returns error if credentials invalid."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        create_user(**payload)
        payload['password'] = 'badpassword'

        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        create_user(**payload)
        payload.pop('password')

        res = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)


class PrivateUsersApiTests(TestCase):
    """Test authenticated API requests."""
    client_class = APIClient

    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_authenticated_registration_faild(self):
        """Test authenticated requests to create user endpoint will be faild."""
        res = self.client.post(CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_login_faild(self):
        """Test authenticated requests to create token endpoints will be faild."""
        res = self.client.post(CREATE_TOKEN_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
