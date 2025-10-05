# apps/mappings/admin.py

from django.contrib import admin
from .models import PatientDoctorMapping

@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    """Admin interface for Patient-Doctor Mapping"""
    list_display = ['patient', 'doctor', 'assigned_by', 'assigned_date', 'is_active']
    list_filter = ['is_active', 'assigned_date']
    search_fields = ['patient__name', 'doctor__name']
    readonly_fields = ['assigned_date']
    
    fieldsets = (
        ('Mapping Details', {
            'fields': ('patient', 'doctor', 'assigned_by')
        }),
        ('Additional Information', {
            'fields': ('notes', 'is_active', 'assigned_date')
        }),
    )