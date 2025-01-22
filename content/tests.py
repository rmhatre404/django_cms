# Test Cases for `content` App
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from content.models import Content

class ContentTests(APITestCase):
    def setUp(self):
        self.content_url = '/api/content/'
        self.user = User.objects.create_user(
            email="author@example.com",
            password="Password@123",
            full_name="Author User",
            phone="1234567890",
            pincode="123456",
            is_author=True
        )
        self.client.force_authenticate(user=self.user)
        self.content_data = {
            "title": "Test Content",
            "body": "This is a test content body.",
            "summary": "Test summary",
            "categories": "Category1, Category2",
        }

    def test_create_content(self):
        """ Test creating content with valid data. """
        response = self.client.post(self.content_url, self.content_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.content_data["title"])

    def test_list_content(self):
        """ Test listing content for an author. """
        Content.objects.create(author=self.user, **self.content_data)
        response = self.client.get(self.content_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_content(self):
        """ Test updating content by its author. """
        content = Content.objects.create(author=self.user, **self.content_data)
        updated_data = {"title": "Updated Title"}
        url = f"{self.content_url}{content.id}/"
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_content(self):
        """ Test deleting content by its author. """
        content = Content.objects.create(author=self.user, **self.content_data)
        url = f"{self.content_url}{content.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_content(self):
        """ Test searching content by title. """
        Content.objects.create(author=self.user, **self.content_data)
        search_url = f"{self.content_url}?search=Test"
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)