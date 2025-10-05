# apps/doctors/models.py

from django.db import models
from django.core.validators import RegexValidator

class Doctor(models.Model):
    """
    Doctor model to store doctor information.
    Doctors are shared resources - any authenticated user can view them.
    
    Note: Doctors don't have a 'created_by' field because they're
    system-wide resources, not owned by individual users.
    """
    
    # Doctor personal information
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    
    # Phone number validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    
    # Professional information
    specialization = models.CharField(
        max_length=100,
        help_text="e.g., Cardiologist, Neurologist, General Physician"
    )
    qualification = models.CharField(max_length=255, help_text="e.g., MBBS, MD, MS")
    experience_years = models.PositiveIntegerField(default=0)
    
    # Professional details
    license_number = models.CharField(max_length=50, unique=True)
    clinic_address = models.TextField()
    
    # Availability
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Consultation fee in your currency"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Is the doctor currently accepting patients?"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doctors'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        ordering = ['name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['specialization']),
            models.Index(fields=['is_available']),
        ]
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"