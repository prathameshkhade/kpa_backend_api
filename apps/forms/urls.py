from django.urls import path
from .views import (WheelSpecificationCreateView)

app_name = 'forms'

urlpatterns = [
    path('wheel-specifications/', WheelSpecificationCreateView.as_view(), name='wheel-specification-create'),
]
