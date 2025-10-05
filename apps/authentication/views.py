# apps/authentication/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationView(APIView):
    """
    API endpoint for user registration.
    
    POST /api/auth/register/
    
    This endpoint is public (no authentication required).
    """
    permission_classes = [AllowAny]  # Anyone can register
    
    def post(self, request):
        """
        Register a new user.
        
        Request body:
        {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "securepass123",
            "password2": "securepass123"
        }
        """
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            # Create the user
            user = serializer.save()
            
            return Response(
                {
                    'message': 'User registered successfully',
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                    }
                },
                status=status.HTTP_201_CREATED
            )
        
        # Return validation errors
        return Response(
            {
                'error': 'Registration failed',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginView(APIView):
    """
    API endpoint for user login.
    
    POST /api/auth/login/
    
    Returns JWT access and refresh tokens.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Authenticate user and return JWT tokens.
        """
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            # validated_data already contains properly formatted response
            data = serializer.validated_data
            
            return Response(
                {
                    'message': 'Login successful',
                    'access': data['access'],
                    'refresh': data['refresh'],
                    'user': data['user'],
                },
                status=status.HTTP_200_OK
            )
        
        return Response(
            {
                'error': 'Login failed',
                'details': serializer.errors
            },
            status=status.HTTP_401_UNAUTHORIZED
        )