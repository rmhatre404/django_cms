from rest_framework import serializers
from users.models import User
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone', 'address', 'city', 'state', 'country', 'pincode', 'is_author']
        read_only_fields = ['id']

    def validate_full_name(self, value):
        """
        Ensures full name includes both first and last names.
        """
        if len(value.split()) < 2:
            raise serializers.ValidationError("Full name must include both first and last names.")
        return value

    def validate_phone(self, value):
        """
        Ensures phone is exactly 10 digits.
        """
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value

    def validate_pincode(self, value):
        """
        Ensures pincode is exactly 6 digits.
        """
        if not re.match(r'^\d{6}$', value):
            raise serializers.ValidationError("Pincode must be exactly 6 digits.")
        return value

    def validate_password(self, value):
        """
        Ensures password meets the required criteria:
        - Minimum 8 characters.
        - At least one uppercase letter.
        - At least one lowercase letter.
        - At least one digit.
        - At least one special character.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value
