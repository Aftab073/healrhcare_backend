# apps/authentication/urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView

"""
Authentication URL patterns.
All auth endpoints are prefixed with /api/auth/
"""

urlpatterns = [
    # User Registration
    # POST /api/auth/register/
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
    # User Login
    # POST /api/auth/login/
    path('login/', UserLoginView.as_view(), name='user-login'),
]