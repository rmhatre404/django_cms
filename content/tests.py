from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from content.models import Content

User = get_user_model()


class ContentAPITestCase(APITestCase):
    def setUp(self):
        # Create a new admin user
        self.admin_user = User.objects.create_superuser(
            email='admin@arcitech.com',
            password='Admin@123',
            full_name='Admin User',
            phone='1234567890',
            pincode='123456'
        )

        # Create a new author user
        self.author_user = User.objects.create_user(
            email='author@arcitech.com',
            password='Author@123',
            full_name='Author User',
            phone='9876543210',
            pincode='654321',
            is_author=True
        )

        # Create content for the author
        self.content = Content.objects.create(
            author=self.author_user,
            title="Test Content",
            body="This is the body of test content.",
            summary="Test summary",
            categories="Test, Example"
        )

    def test_admin_can_view_all_content(self):
        # Admin login
        self.client.login(email='admin@arcitech.com', password='Admin@123')

        # Admin retrieves all content
        response = self.client.get('/api/content/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Admin can view all content

    def test_author_can_view_own_content(self):
        # Author login
        self.client.login(email='author@arcitech.com', password='Author@123')

        # Author retrieves their own content
        response = self.client.get('/api/content/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Author can only view their own content

    def test_author_cannot_view_others_content(self):
        # Create another author and content
        other_author = User.objects.create_user(
            email='other@arcitech.com',
            password='Other@123',
            full_name='Other Author',
            phone='1112223334',
            pincode='111111',
            is_author=True
        )
        Content.objects.create(
            author=other_author,
            title="Other Content",
            body="This is the body of other content.",
            summary="Other summary",
            categories="Other"
        )

        # Author login
        self.client.login(email='author@arcitech.com', password='Author@123')

        # Author should not see other author's content
        response = self.client.get('/api/content/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only their own content is visible

    def test_author_can_create_content(self):
        # Author login
        self.client.login(email='author@arcitech.com', password='Author@123')

        # Create new content
        response = self.client.post('/api/content/', {
            "title": "New Content",
            "body": "This is the body of new content.",
            "summary": "New summary",
            "categories": "Category1, Category2"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Content")

    def test_admin_can_update_content(self):
        # Admin login
        self.client.login(email='admin@arcitech.com', password='Admin@123')

        # Update content created by the author
        response = self.client.put(f'/api/content/{self.content.id}/', {
            "title": "Updated Content Title",
            "body": "Updated content body.",
            "summary": "Updated summary",
            "categories": "Updated, Category"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Content Title")

    def test_author_can_delete_own_content(self):
        # Author login
        self.client.login(email='author@arcitech.com', password='Author@123')

        # Delete their own content
        response = self.client.delete(f'/api/content/{self.content.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_delete_any_content(self):
        # Admin login
        self.client.login(email='admin@arcitech.com', password='Admin@123')

        # Delete content created by the author
        response = self.client.delete(f'/api/content/{self.content.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_user_cannot_access_content(self):
        # Attempt to retrieve content without logging in
        response = self.client.get('/api/content/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
