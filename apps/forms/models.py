from django.db import models
from apps.common.models import TimestampedModel

class WheelSpecification(TimestampedModel):
    """Model for storing wheel specifications."""

    # Form metadata
    form_number = models.CharField(max_length=50, unique=True, db_index=True)
    submitted_by = models.CharField(max_length=100)
    submitted_date = models.DateField()
    status = models.CharField(max_length=20, default='saved')

    # Technical specifications
    tread_diameter_new = models.CharField(max_length=50, help_text="e.g., 915 (900-1000)")
    last_shop_issue_size = models.CharField(max_length=50, help_text="e.g., 837 (800-900)")
    condemning_dia = models.CharField(max_length=50, help_text="e.g., 825 (800-900)")
    wheel_gauge = models.CharField(max_length=50, help_text="e.g., 1600 (+2,-1)")
    variation_same_axle = models.CharField(max_length=20)
    variation_same_bogie = models.CharField(max_length=20)
    variation_same_coach = models.CharField(max_length=20)
    wheel_profile = models.CharField(max_length=100)
    intermediate_wwp = models.CharField(max_length=50)
    bearing_seat_diameter = models.CharField(max_length=50)
    roller_bearing_outer_dia = models.CharField(max_length=50)
    roller_bearing_bore_dia = models.CharField(max_length=50)
    roller_bearing_width = models.CharField(max_length=50)
    axle_box_housing_bore_dia = models.CharField(max_length=50)
    wheel_disc_width = models.CharField(max_length=50)

    class Meta:
        db_table = 'wheel_specification'
        ordering = ['-created_at']
        verbose_name = "Wheel Specification"
        verbose_name_plural = "Wheel Specifications"

    def __str__(self):
        return f'{self.form_number} - {self.submitted_by} on {self.submitted_date}'