# apps/patients/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet

"""
Patient URL patterns.
All patient endpoints are prefixed with /api/patients/

Using DRF Router for automatic URL generation.
"""

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'', PatientViewSet, basename='patient')

"""
The router automatically generates these URLs:
- POST   /api/patients/          -> create a patient
- GET    /api/patients/          -> list all patients
- GET    /api/patients/{id}/     -> retrieve a patient
- PUT    /api/patients/{id}/     -> update a patient
- PATCH  /api/patients/{id}/     -> partial update a patient
- DELETE /api/patients/{id}/     -> delete a patient
"""

urlpatterns = [
    path('', include(router.urls)),
]