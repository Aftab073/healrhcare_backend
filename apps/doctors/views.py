# apps/doctors/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer, DoctorListSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctors.
    
    Provides CRUD operations:
    - POST /api/doctors/ - Create a doctor
    - GET /api/doctors/ - List all doctors
    - GET /api/doctors/{id}/ - Retrieve a specific doctor
    - PUT /api/doctors/{id}/ - Update a doctor
    - PATCH /api/doctors/{id}/ - Partial update
    - DELETE /api/doctors/{id}/ - Delete a doctor
    
    All endpoints require authentication.
    Note: Unlike patients, doctors are system-wide resources.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    
    def get_serializer_class(self):
        """
        Use lightweight serializer for list view.
        """
        if self.action == 'list':
            return DoctorListSerializer
        return DoctorSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new doctor.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Doctor created successfully',
                    'doctor': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'error': 'Failed to create doctor',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific doctor.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def update(self, request, *args, **kwargs):
        """
        Update a doctor (full update - PUT).
        """
        partial = kwargs.pop('partial', False)
        
        try:
            instance = self.get_object()
        except Doctor.DoesNotExist:
            return Response(
                {'error': 'Doctor not found'},
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
                    'message': 'Doctor updated successfully',
                    'doctor': serializer.data
                }
            )
        
        return Response(
            {
                'error': 'Failed to update doctor',
                'details': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partial update a doctor (PATCH).
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a doctor.
        """
        try:
            instance = self.get_object()
            instance.delete()
            return Response(
                {'message': 'Doctor deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Doctor.DoesNotExist:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def list(self, request, *args, **kwargs):
        """
        List all doctors.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
            {
                'count': queryset.count(),
                'doctors': serializer.data
            }
        )