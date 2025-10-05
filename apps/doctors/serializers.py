# apps/doctors/serializers.py

from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model.
    Handles CRUD operations for doctors.
    """
    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'email',
            'phone_number',
            'specialization',
            'qualification',
            'experience_years',
            'license_number',
            'clinic_address',
            'consultation_fee',
            'is_available',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_email(self, value):
        """
        Ensure email is unique for doctors.
        """
        instance = self.instance
        
        if instance:
            # Updating
            if Doctor.objects.exclude(pk=instance.pk).filter(email=value).exists():
                raise serializers.ValidationError(
                    "A doctor with this email already exists."
                )
        else:
            # Creating
            if Doctor.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    "A doctor with this email already exists."
                )
        
        return value
    
    def validate_license_number(self, value):
        """
        Ensure license number is unique.
        """
        instance = self.instance
        
        if instance:
            # Updating
            if Doctor.objects.exclude(pk=instance.pk).filter(license_number=value).exists():
                raise serializers.ValidationError(
                    "A doctor with this license number already exists."
                )
        else:
            # Creating
            if Doctor.objects.filter(license_number=value).exists():
                raise serializers.ValidationError(
                    "A doctor with this license number already exists."
                )
        
        return value
    
    def validate_experience_years(self, value):
        """
        Ensure experience years is not negative.
        """
        if value < 0:
            raise serializers.ValidationError(
                "Experience years cannot be negative."
            )
        return value
    
    def validate_consultation_fee(self, value):
        """
        Ensure consultation fee is positive.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Consultation fee must be greater than zero."
            )
        return value


class DoctorListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing doctors.
    """
    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'specialization',
            'experience_years',
            'consultation_fee',
            'is_available'
        ]