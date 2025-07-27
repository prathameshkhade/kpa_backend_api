from rest_framework import serializers
from .models import WheelSpecification

class WheelSpecificationFieldsSerializer(serializers.Serializer):
    """Nested serializer for wheel specification fields"""
    treadDiameterNew = serializers.CharField(max_length=50, source='tread_diameter_new')
    lastShopIssueSize = serializers.CharField(max_length=50, source='last_shop_issue_size')
    condemningDia = serializers.CharField(max_length=50, source='condemning_dia')
    wheelGauge = serializers.CharField(max_length=50, source='wheel_gauge')
    variationSameAxle = serializers.CharField(max_length=20, source='variation_same_axle')
    variationSameBogie = serializers.CharField(max_length=20, source='variation_same_bogie')
    variationSameCoach = serializers.CharField(max_length=20, source='variation_same_coach')
    wheelProfile = serializers.CharField(max_length=100, source='wheel_profile')
    intermediateWWP = serializers.CharField(max_length=50, source='intermediate_wwp')
    bearingSeatDiameter = serializers.CharField(max_length=50, source='bearing_seat_diameter')
    rollerBearingOuterDia = serializers.CharField(max_length=50, source='roller_bearing_outer_dia')
    rollerBearingBoreDia = serializers.CharField(max_length=50, source='roller_bearing_bore_dia')
    rollerBearingWidth = serializers.CharField(max_length=50, source='roller_bearing_width')
    axleBoxHousingBoreDia = serializers.CharField(max_length=50, source='axle_box_housing_bore_dia')
    wheelDiscWidth = serializers.CharField(max_length=50, source='wheel_disc_width')

class WheelSpecificationSerializer(serializers.ModelSerializer):
    """Main serializer for WheelSpecification model."""
    formNumber = serializers.CharField(source='form_number')
    submittedBy = serializers.CharField(source='submitted_by')
    submittedDate = serializers.DateField(source='submitted_date')
    fields = WheelSpecificationFieldsSerializer(source='*')
    status = serializers.CharField(read_only=True)

    class Meta:
        model = WheelSpecification
        fields = ['formNumber', 'submittedBy', 'submittedDate', 'fields', 'status',]

    def create(self, validated_data):
        """Create a new WheelSpecification instance."""
        fields_data = validated_data.pop('*', {})
        validated_data.update(fields_data)
        return WheelSpecification.objects.create(**validated_data)

    def validate_formNumber(self, value):
        """Validate formNumber format"""
        if not value.startswith('WHEEL-'):
            raise serializers.ValidationError("Form number must start with 'WHEEL-'")
        return value
    
class WheelSpecificationResponseSerializer(serializers.ModelSerializer):
    """Response serializer for wheel specifications"""
    formNumber = serializers.CharField(source='form_number')    
    submittedBy = serializers.CharField(source='submitted_by')
    submittedDate = serializers.DateField(source='submitted_date')
    status = serializers.CharField()

    class Meta: 
        model = WheelSpecification
        fields = ['formNumber', 'submittedBy', 'submittedDate', 'status']


class WheelSpecificationListViewSerializer(serializers.ModelSerializer):
    """Serializer for listing wheel specifications with filtering options."""
    formNumber = serializers.CharField(source='form_number')
    submittedBy = serializers.CharField(source='submitted_by')
    submittedDate = serializers.DateField(source='submitted_date')
    wheelFields = serializers.SerializerMethodField()
    status = serializers.CharField()

    class Meta:
        model = WheelSpecification
        fields = ['formNumber', 'submittedBy', 'submittedDate', 'wheelFields', 'status']

    def get_wheelFields(self, obj):
        """Get wheel specification fields"""
        return {
            "condemningDia": obj.condemning_dia,
            "lastShopIssueSize": obj.last_shop_issue_size,
            "treadDiameterNew": obj.tread_diameter_new,
            "wheelGauge": obj.wheel_gauge,
        }
