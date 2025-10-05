# apps/doctors/admin.py

from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Admin interface for Doctor model"""
    list_display = ['name', 'specialization', 'email', 'phone_number', 'experience_years', 'is_available']
    list_filter = ['specialization', 'is_available', 'created_at']
    search_fields = ['name', 'email', 'specialization', 'license_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone_number')
        }),
        ('Professional Information', {
            'fields': ('specialization', 'qualification', 'experience_years', 'license_number')
        }),
        ('Practice Details', {
            'fields': ('clinic_address', 'consultation_fee', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )