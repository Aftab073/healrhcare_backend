# apps/authentication/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    We're using email as the unique identifier instead of username.
    
    Why custom user model?
    - Flexibility to add fields later
    - Better control over authentication
    - Industry best practice
    """
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    
    # We'll use email for login instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']  # username still required by Django internally
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email