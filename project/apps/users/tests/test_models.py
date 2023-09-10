"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest.mock import patch

from project.apps.users import models

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_successful(self):
        """Test creating a user is successful."""
        username = 'testUserName'
        email = 'test@example.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )

        is_user_exists = get_user_model().objects.get(username=username)


        self.assertTrue(is_user_exists)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normilized(self):
        """Test email is normilized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]


        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(username='testUserName', email=email, password='testpass123')
            self.assertEqual(user.email, expected)
            user.delete()

    def test_create_user_without_email_raises_error(self):
        """Test creating a user without an email raises a ValueError."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(username='testUsername', email='', password='testpass123')

    def test_create_user_without_username_raises_error(self):
        """Test creating a user without username raises a ValueError."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(username='', email='test@example.com', password='testpass123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            username='testUserName',
            email='test@example.com',
            password='testpass123'
        )

        self.assertTrue(user.is_superuser)

    @patch('project.apps.users.models.uuid.uuid4')
    def test_user_avatar_file_name_uuid(self, mock_uuid):
        """Test generate user avatar file path."""
        uuid = 'test-uuid4'
        mock_uuid.return_value = uuid

        file_path = models.user_avatar_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/avatar/{uuid}.jpg')
