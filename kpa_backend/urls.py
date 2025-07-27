from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),

    # api/forms
    path('api/forms/', include('apps.forms.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Helth check
    path('health/', lambda request: JsonResponse({'status': 'ok', 'message': 'API is running'}), name='health_check'),
]
