# apps/authentication/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles password validation and hashing.
    """
    password = serializers.CharField(
        write_only=True,  # Password won't be included in response
        required=True,
        validators=[validate_password],  # Use Django's password validators
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirm Password'
    )
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'password2']
        read_only_fields = ['id']
    
    def validate(self, attrs):
        """
        Validate that both passwords match.
        This method is called before create().
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs
    
    def create(self, validated_data):
        """
        Create and return a new user with encrypted password.
        """
        # Remove password2 as it's not a field in the model
        validated_data.pop('password2')
        
        # Create user with hashed password
        user = User.objects.create_user(
            username=validated_data['email'],  # Using email as username
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Returns JWT tokens upon successful authentication.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    # These fields will be returned in the response
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    
    def get_user(self, obj):
        """
        Return basic user information.
        """
        return {
            'id': obj['user'].id,
            'email': obj['user'].email,
            'name': obj['user'].name,
        }
    
    def validate(self, attrs):
        """
        Validate credentials and generate tokens.
        """
        email = attrs.get('email')
        password = attrs.get('password')
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'error': 'Invalid credentials. Please check your email and password.'
            })
        
        # Check if password is correct
        if not user.check_password(password):
            raise serializers.ValidationError({
                'error': 'Invalid credentials. Please check your email and password.'
            })
        
        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError({
                'error': 'User account is disabled.'
            })
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return {
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer for displaying user information.
    """
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']