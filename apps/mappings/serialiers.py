# apps/mappings/serializers.py

from rest_framework import serializers
from .models import PatientDoctorMapping
from apps.patients.models import Patient
from apps.doctors.serializers import DoctorSerializer
from apps.patients.serializers import PatientListSerializer

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and managing patient-doctor mappings.
    """
    # Display full details in responses
    patient_details = PatientListSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.name', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id',
            'patient',
            'doctor',
            'patient_details',
            'doctor_details',
            'assigned_by',
            'assigned_by_name',
            'assigned_date',
            'notes',
            'is_active'
        ]
        read_only_fields = ['id', 'assigned_by', 'assigned_date']
    
    def validate(self, attrs):
        """
        Validate the mapping before creation.
        """
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        # Check if patient exists and belongs to the requesting user
        request = self.context.get('request')
        if request and request.user:
            if patient.created_by != request.user:
                raise serializers.ValidationError({
                    'patient': 'You can only assign doctors to your own patients.'
                })
        
        # Check if mapping already exists (when creating)
        if not self.instance:
            if PatientDoctorMapping.objects.filter(
                patient=patient,
                doctor=doctor
            ).exists():
                raise serializers.ValidationError({
                    'error': 'This patient is already assigned to this doctor.'
                })
        
        return attrs
    
    def create(self, validated_data):
        """
        Create a new patient-doctor mapping.
        """
        return PatientDoctorMapping.objects.create(**validated_data)


class PatientDoctorListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing mappings.
    """
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id',
            'patient_name',
            'doctor_name',
            'doctor_specialization',
            'assigned_date',
            'is_active'
        ]


class DoctorsByPatientSerializer(serializers.Serializer):
    """
    Serializer for retrieving all doctors assigned to a patient.
    """
    patient_id = serializers.IntegerField()
    patient_name = serializers.CharField()
    doctors = DoctorSerializer(many=True)
    total_doctors = serializers.IntegerField()