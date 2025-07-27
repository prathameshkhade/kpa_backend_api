from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import WheelSpecificationSerializer, WheelSpecificationResponseSerializer
from drf_spectacular.utils import extend_schema

from .models import WheelSpecification
from .serializers import (
    WheelSpecificationSerializer,
    WheelSpecificationResponseSerializer
)

class WheelSpecificationCreateView(generics.CreateAPIView):
    """Create WheelSpecification end point."""
    queryset = WheelSpecification.objects.all()
    serializer_class = WheelSpecificationSerializer

    @extend_schema(
        summary="Create a new Wheel Specification",
        description="Submit a new wheel specification form.",
        responses={
            201: WheelSpecificationResponseSerializer,
            400: {
                "type": 'object',
                "properties": {
                    "field_name": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                }
            }
        }
    )
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = WheelSpecificationResponseSerializer(instance)  # Fix here - use the instance instead of int
    
            response = {
                "success": True,
                "message": "Wheel specification submitted successfully.",
                "data": response_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
