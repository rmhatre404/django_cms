from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone', 'address', 'city', 'state', 'country', 'pincode', 'is_author']
        read_only_fields = ['id']

