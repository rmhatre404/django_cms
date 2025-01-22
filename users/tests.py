# Test Cases for `users` App

from rest_framework.test import APITestCase
from rest_framework import status

class UserTests(APITestCase):
    def setUp(self):
        self.register_url = '/api/users/register/'
        self.login_url = '/api/users/login/'
        self.user_data = {
            "email": "testuser@example.com",
            "password": "Password@123",
            "full_name": "Test User",
            "phone": "1234567890",
            "pincode": "123456"
        }

    def test_register_valid_user(self):
        """ Test user registration with valid data. """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_invalid_password(self):
        """ Test registration with invalid password. """
        invalid_data = self.user_data.copy()
        invalid_data["password"] = "short"
        response = self.client.post(self.register_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Adjusted to check the error message in the response
        self.assertIn("Password must be at least 8 characters long.", str(response.data))

    def test_login_valid_user(self):
        """ Test login with valid credentials. """
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_invalid_user(self):
        """ Test login with invalid credentials. """
        login_data = {
            "email": "nonexistent@example.com",
            "password": "Password@123"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)