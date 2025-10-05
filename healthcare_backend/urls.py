# healthcare_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    """
    Root API endpoint - provides an overview of available endpoints.
    """
    return JsonResponse({
        'message': 'Welcome to Healthcare Backend API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'register': '/api/auth/register/',
                'login': '/api/auth/login/',
            },
            'patients': {
                'base': '/api/patients/',
                'detail': '/api/patients/{id}/',
            },
            'doctors': {
                'base': '/api/doctors/',
                'detail': '/api/doctors/{id}/',
            },
            'mappings': {
                'base': '/api/mappings/',
                'assign': '/api/mappings/',
                'by_patient': '/api/mappings/{patient_id}/',
                'remove': '/api/mappings/{id}/',
            }
        },
        'documentation': '/admin/',
    })

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API Root - informational endpoint
    path('api/', api_root, name='api-root'),
    
    # Authentication endpoints
    path('api/auth/', include('apps.authentication.urls')),
    
    # Patient endpoints
    path('api/patients/', include('apps.patients.urls')),
    
    # Doctor endpoints
    path('api/doctors/', include('apps.doctors.urls')),
    
    # Patient-Doctor Mapping endpoints
    path('api/mappings/', include('apps.mappings.urls')),
]