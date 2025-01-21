from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Use the dynamic user model

class Content(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contents")
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.CharField(max_length=60)
    categories = models.CharField(max_length=100)  # Comma-separated categories
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
