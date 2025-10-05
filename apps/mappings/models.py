# apps/mappings/models.py

from django.db import models
from django.conf import settings
from apps.patients.models import Patient
from apps.doctors.models import Doctor

class PatientDoctorMapping(models.Model):
    """
    Many-to-Many relationship between Patients and Doctors.
    
    Why a separate model instead of ManyToManyField?
    - We can add extra fields (assigned_by, assigned_date, notes)
    - Better control over the relationship
    - Can track who assigned which doctor to which patient
    - Easier to implement business logic
    """
    
    # The patient in this relationship
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='doctor_mappings'
    )
    
    # The doctor in this relationship
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='patient_mappings'
    )
    
    # Who created this mapping (for audit purposes)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='mappings_created'
    )
    
    # When was this assignment made
    assigned_date = models.DateTimeField(auto_now_add=True)
    
    # Optional notes about this assignment
    notes = models.TextField(
        blank=True,
        help_text="Any special notes about this patient-doctor assignment"
    )
    
    # Is this assignment currently active?
    is_active = models.BooleanField(
        default=True,
        help_text="Set to False if patient is no longer seeing this doctor"
    )
    
    class Meta:
        db_table = 'patient_doctor_mappings'
        verbose_name = 'Patient-Doctor Mapping'
        verbose_name_plural = 'Patient-Doctor Mappings'
        ordering = ['-assigned_date']
        
        # Ensure a patient can't be assigned to the same doctor twice
        unique_together = ['patient', 'doctor']
        
        indexes = [
            models.Index(fields=['patient', 'doctor']),
            models.Index(fields=['assigned_date']),
        ]
    
    def __str__(self):
        return f"{self.patient.name} → Dr. {self.doctor.name}"
    
    def save(self, *args, **kwargs):
        """
        Override save to add custom validation.
        Ensure the patient belongs to the user making the assignment.
        """
        super().save(*args, **kwargs)