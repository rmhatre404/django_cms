from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Seed Admin User'

    def handle(self, *args, **kwargs):
        admin_email = 'admin@arcitech.com'
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                password='Admin@123',
                full_name='Arcitech Admin User',
                phone='1234567890',
                pincode='123456',
                is_author=False
            )
            self.stdout.write(self.style.SUCCESS(f"Admin user '{admin_email}' created."))
        else:
            self.stdout.write(self.style.WARNING(f"Admin user '{admin_email}' already exists."))
