from django.urls import path
from .views import WheelSpecificationListCreateView

app_name = 'forms'

urlpatterns = [
    path('wheel-specifications/', WheelSpecificationListCreateView.as_view(), name='wheel-specification'),
]
