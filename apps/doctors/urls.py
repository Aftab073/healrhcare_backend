# apps/doctors/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet

"""
Doctor URL patterns.
All doctor endpoints are prefixed with /api/doctors/

Using DRF Router for automatic URL generation.
"""

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'', DoctorViewSet, basename='doctor')

"""
The router automatically generates these URLs:
- POST   /api/doctors/          -> create a doctor
- GET    /api/doctors/          -> list all doctors
- GET    /api/doctors/{id}/     -> retrieve a doctor
- PUT    /api/doctors/{id}/     -> update a doctor
- PATCH  /api/doctors/{id}/     -> partial update a doctor
- DELETE /api/doctors/{id}/     -> delete a doctor
"""

urlpatterns = [
    path('', include(router.urls)),
]