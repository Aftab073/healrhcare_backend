# apps/patients/admin.py

from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Admin interface for Patient model"""
    list_display = ['name', 'email', 'phone_number', 'blood_group', 'created_by', 'created_at']
    list_filter = ['blood_group', 'created_at']
    search_fields = ['name', 'email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone_number', 'date_of_birth', 'address')
        }),
        ('Medical Information', {
            'fields': ('blood_group', 'medical_history')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )