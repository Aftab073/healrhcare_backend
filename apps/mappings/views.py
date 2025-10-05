# apps/mappings/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from .serializers import (
    PatientDoctorMappingSerializer,
    PatientDoctorListSerializer,
    DoctorsByPatientSerializer
)
from apps.patients.models import Patient
from apps.doctors.serializers import DoctorSerializer

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patient-doctor mappings.
    
    Endpoints:
    - POST /api/mappings/ - Assign a doctor to a patient
    - GET /api/mappings/ - List all mappings
    - GET /api/mappings/{patient_id}/ - Get doctors for a specific patient
    - DELETE /api/mappings/{id}/ - Remove a doctor from a patient
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PatientDoctorMappingSerializer
    
    def get_queryset(self):
        """
        Return mappings only for patients created by current user.
        """
        # Get all patients created by current user
        user_patients = Patient.objects.filter(created_by=self.request.user)
        
        # Return mappings for those patients
        return PatientDoctorMapping.objects.filter(
            patient__in=user_patients
        ).select_related('patient', 'doctor', 'assigned_by')
    
    def get_serializer_class(self):
        """
        Use appropriate serializer based on action.
        """
        if self.action == 'list':
            return PatientDoctorListSerializer
        elif self.action == 'doctors_by_patient':
            return DoctorsByPatientSerializer
        return PatientDoctorMappingSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new patient-doctor mapping.
        Assign a doctor to a patient.
        """
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Set assigned_by to current user
            serializer.save(assigned_by=request.user)
            
            return Response(
                {
                    'message': 'Doctor assigned to patient successfully',
                    'mapping': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'error': 'Failed to assign doctor to patient',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        """
        List all patient-doctor mappings for current user's patients.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
            {
                'count': queryset.count(),
                'mappings': serializer.data
            }
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get all doctors assigned to a specific patient.
        URL: GET /api/mappings/{patient_id}/
        
        Note: The pk here represents patient_id, not mapping_id.
        This matches the assignment requirement.
        """
        patient_id = kwargs.get('pk')
        
        # Verify patient exists and belongs to current user
        patient = get_object_or_404(
            Patient,
            id=patient_id,
            created_by=request.user
        )
        
        # Get all doctors assigned to this patient
        mappings = PatientDoctorMapping.objects.filter(
            patient=patient,
            is_active=True
        ).select_related('doctor')
        
        # Extract doctors from mappings
        doctors = [mapping.doctor for mapping in mappings]
        doctor_serializer = DoctorSerializer(doctors, many=True)
        
        return Response(
            {
                'patient_id': patient.id,
                'patient_name': patient.name,
                'total_doctors': len(doctors),
                'doctors': doctor_serializer.data
            }
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Remove a doctor from a patient.
        Delete a specific mapping by mapping ID.
        """
        try:
            instance = self.get_object()
            
            # Store info for response message
            patient_name = instance.patient.name
            doctor_name = instance.doctor.name
            
            instance.delete()
            
            return Response(
                {
                    'message': f'Dr. {doctor_name} removed from patient {patient_name} successfully'
                },
                status=status.HTTP_204_NO_CONTENT
            )
        except PatientDoctorMapping.DoesNotExist:
            return Response(
                {'error': 'Mapping not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='patient/(?P<patient_id>[^/.]+)')
    def doctors_by_patient(self, request, patient_id=None):
        """
        Alternative endpoint to get doctors by patient ID.
        URL: GET /api/mappings/patient/{patient_id}/
        
        This provides an alternative to the retrieve method.
        """
        # Verify patient exists and belongs to current user
        patient = get_object_or_404(
            Patient,
            id=patient_id,
            created_by=request.user
        )
        
        # Get all active doctors for this patient
        mappings = PatientDoctorMapping.objects.filter(
            patient=patient,
            is_active=True
        ).select_related('doctor')
        
        doctors = [mapping.doctor for mapping in mappings]
        doctor_serializer = DoctorSerializer(doctors, many=True)
        
        data = {
            'patient_id': patient.id,
            'patient_name': patient.name,
            'total_doctors': len(doctors),
            'doctors': doctor_serializer.data
        }
        
        return Response(data)