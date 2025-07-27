from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import WheelSpecificationSerializer, WheelSpecificationResponseSerializer, WheelSpecificationListViewSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import WheelSpecification

class WheelSpecificationListCreateView(generics.ListCreateAPIView):
    """List and Create WheelSpecifications"""
    queryset = WheelSpecification.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['form_number', 'submitted_by', 'submitted_date']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WheelSpecificationSerializer
        return WheelSpecificationListViewSerializer

    @extend_schema(
        summary="List Wheel Specifications",
        description="Retrieve wheel specifications with optional filtering",
        parameters=[
            OpenApiParameter('formNumber', type=str, description="Filter by form number"),
            OpenApiParameter('submittedBy', type=str, description="Filter by submitted by"),
            OpenApiParameter('submittedDate', type=str, description="Filter by submitted date (YYYY-MM-DD)"),
        ],
        responses={200: WheelSpecificationListViewSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        form_number = request.query_params.get('formNumber')
        submitted_by = request.query_params.get('submittedBy')
        submitted_date = request.query_params.get('submittedDate')

        if form_number:
            queryset = queryset.filter(form_number=form_number)
        if submitted_by:
            queryset = queryset.filter(submitted_by=submitted_by)
        if submitted_date:
            queryset = queryset.filter(submitted_date=submitted_date)

        serializer = self.get_serializer(queryset, many=True)

        res = {
            "success": True,
            "message": "Filtered wheel specification forms fetched successfully.",
            "data": serializer.data
        }

        return Response(res, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a new Wheel Specification",
        description="Submit a new wheel specification form.",
        responses={201: WheelSpecificationResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_serializer = WheelSpecificationResponseSerializer(instance)
    
            response = {
                "success": True,
                "message": "Wheel specification submitted successfully.",
                "data": response_serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
