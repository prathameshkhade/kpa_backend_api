from django.db import models

class TimestampedModel(models.Model):
    """Abstract base model that provides created and modified timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
