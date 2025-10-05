# apps/mappings/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientDoctorMappingViewSet

"""
Patient-Doctor Mapping URL patterns.
All mapping endpoints are prefixed with /api/mappings/

Using DRF Router for automatic URL generation.
"""

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'', PatientDoctorMappingViewSet, basename='mapping')

"""
The router automatically generates these URLs:
- POST   /api/mappings/              -> assign doctor to patient
- GET    /api/mappings/              -> list all mappings
- GET    /api/mappings/{patient_id}/ -> get all doctors for a patient
- DELETE /api/mappings/{id}/         -> remove doctor from patient

Additional custom endpoint:
- GET    /api/mappings/patient/{patient_id}/ -> alternative way to get doctors by patient
"""

urlpatterns = [
    path('', include(router.urls)),
]