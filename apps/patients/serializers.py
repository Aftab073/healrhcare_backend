# apps/patients/serializers.py

from rest_framework import serializers
from .models import Patient
from apps.authentication.serializers import UserSerializer

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    Handles CRUD operations for patients.
    """
    # Display creator information in responses
    created_by_details = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'email',
            'phone_number',
            'address',
            'date_of_birth',
            'blood_group',
            'medical_history',
            'created_by',
            'created_by_details',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def validate_email(self, value):
        """
        Check that email is unique when creating or updating.
        """
        # Get the instance being updated (None for create)
        instance = self.instance
        
        # Check if email already exists for a different patient
        if instance:
            # Updating - exclude current instance from uniqueness check
            if Patient.objects.exclude(pk=instance.pk).filter(email=value).exists():
                raise serializers.ValidationError(
                    "A patient with this email already exists."
                )
        else:
            # Creating - check if email exists
            if Patient.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    "A patient with this email already exists."
                )
        
        return value
    
    def create(self, validated_data):
        """
        Create a new patient.
        The 'created_by' field is set in the view.
        """
        return Patient.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update patient information.
        """
        # Update all fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance


class PatientListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing patients.
    Excludes heavy fields like medical_history.
    """
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'email',
            'phone_number',
            'blood_group',
            'created_by_name',
            'created_at'
        ]