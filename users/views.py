from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError


class AuthorRegistrationView(APIView):
    """
    Handles the registration of new author users.
    - Validates the input data using the UserSerializer.
    - Automatically marks the user as an author (`is_author=True`).
    - Hashes the user's password before saving to the database.
    """

    def post(self, request):
        data = request.data
        data['is_author'] = True  # Ensure the user is marked as an author

        # Use the serializer to validate the data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            try:
                # Validate password separately
                password = data.get('password')
                if not password:
                    return Response({"password": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

                # Use the custom password validator
                serializer.validate_password(password)
            except ValidationError as e:
                return Response({"password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

            # Save the user instance but do not commit to the database yet
            user = serializer.save()
            # Hash the password before saving the user
            user.set_password(password)
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handles user login.
    - Verifies the provided email and password.
    - Issues a JWT token (access and refresh) upon successful authentication.
    """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # print("Login Attempt:", email, password)  # Debugging

        try:
            # Retrieve the user by email
            user = User.objects.get(email=email)
            #print("Found User:", user.email, user.password)  # Debugging
        except User.DoesNotExist:
            # Return an error if the user is not found
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if the provided password matches the hashed password in the database
        if not user.check_password(password):
            print("Password Check Failed")  # Debugging
            return Response({"detail": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
