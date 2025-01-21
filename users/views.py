# from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

class AuthorRegistrationView(APIView):
    def post(self, request):
        data = request.data
        print("Registration Data Received:", data)  # Debugging
        data['is_author'] = True
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            print("Before Password Hashing:", user.password)  # Debugging
            user.set_password(data['password'])
            user.save()
            print("After Password Hashing:", user.password)  # Debugging
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Registration Errors:", serializer.errors)  # Debugging
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print("Login Attempt:", email, password)  # Debugging

        try:
            user = User.objects.get(email=email)
            print("Found User:", user.email, user.password)  # Debugging
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)

        if not user.check_password(password):
            print("Password Check Failed")  # Debugging
            return Response({"detail": "Incorrect password"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=200)
