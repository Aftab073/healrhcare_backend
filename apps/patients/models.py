# apps/patients/models.py

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class Patient(models.Model):
    """
    Patient model to store patient information.
    Each patient is created by a user (creator).
    
    Important: Patients belong to users, not doctors.
    The relationship with doctors is through the Mapping model.
    """
    
    # Relationship with User who created this patient
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patients'
    )
    
    # Patient personal information
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    
    # Phone number validation (10 digits)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Address fields
    address = models.TextField(blank=True)
    
    # Medical information
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('O+', 'O+'), ('O-', 'O-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
        ],
        blank=True
    )
    medical_history = models.TextField(blank=True, help_text="Any relevant medical history")
    
    # Timestamps - automatically managed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'patients'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_by', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.email}"