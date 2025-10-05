# apps/patients/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer, PatientListSerializer

class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patients.
    
    Provides CRUD operations:
    - POST /api/patients/ - Create a patient
    - GET /api/patients/ - List all patients (created by current user)
    - GET /api/patients/{id}/ - Retrieve a specific patient
    - PUT /api/patients/{id}/ - Update a patient
    - PATCH /api/patients/{id}/ - Partial update
    - DELETE /api/patients/{id}/ - Delete a patient
    
    All endpoints require authentication.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PatientSerializer
    
    def get_queryset(self):
        """
        Return only patients created by the current user.
        This ensures users can only see their own patients.
        """
        return Patient.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        """
        Use lightweight serializer for list view.
        Use full serializer for detail views and create/update.
        """
        if self.action == 'list':
            return PatientListSerializer
        return PatientSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new patient.
        Automatically set the created_by field to current user.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Set the created_by field to current user
            serializer.save(created_by=request.user)
            
            return Response(
                {
                    'message': 'Patient created successfully',
                    'patient': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'error': 'Failed to create patient',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific patient.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, *args, **kwargs):
        """
        Update a patient (full update - PUT).
        """
        partial = kwargs.pop('partial', False)
        
        try:
            instance = self.get_object()
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Patient updated successfully',
                    'patient': serializer.data
                }
            )
        
        return Response(
            {
                'error': 'Failed to update patient',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update a patient (PATCH).
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a patient.
        """
        try:
            instance = self.get_object()
            instance.delete()
            return Response(
                {'message': 'Patient deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Patient.DoesNotExist:
            return Response(
                {'error': 'Patient not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def list(self, request, *args, **kwargs):
        """
        List all patients created by current user.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
            {
                'count': queryset.count(),
                'patients': serializer.data
            }
        )