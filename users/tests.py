from django.test import TestCase

# Create your tests here.
from django.core.management import call_command
from django.test import TestCase
from users.models import User


class SeedAdminCommandTest(TestCase):
    def test_seed_admin_creates_admin_user(self):
        """
        Test that the seed_admin command creates an admin user if one does not exist.
        """
        admin_email = "admin@arcitech.com"

        # Ensure the admin user does not exist initially
        self.assertFalse(User.objects.filter(email=admin_email).exists())

        # Call the seed_admin command
        call_command('seed_admin')

        # Verify the admin user is created
        admin_user = User.objects.get(email=admin_email)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertFalse(admin_user.is_author)

    def test_seed_admin_does_not_duplicate_existing_admin_user(self):
        """
        Test that the seed_admin command does not create duplicate admin users.
        """
        admin_email = "admin@arcitech.com"

        # Pre-create the admin user
        User.objects.create_superuser(
            email=admin_email,
            password="Admin@123",
            full_name="Arcitech Admin User",
            phone="1234567890",
            pincode="123456",
            is_author=False
        )

        # Call the seed_admin command
        call_command('seed_admin')

        # Verify no duplicate admin user is created
        admin_users = User.objects.filter(email=admin_email)
        self.assertEqual(admin_users.count(), 1)
