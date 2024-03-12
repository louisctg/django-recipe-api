"""
Tests for user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """Helper function to create a user."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Tests for the user API (public)."""

    def setUp(self):
        """Create client."""
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating a user with valid payload, is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_with_email_exists(self):
        """Test creating a user that already exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test whether error returned when password is less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pwd',
            'name': 'Test User',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
