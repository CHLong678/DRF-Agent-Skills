"""Typed DRF serializer examples.

Baseline: Django 3.2+ and a DRF version compatible with the installed Django.
"""

from django.db import models
from rest_framework import serializers


class OrderStatus(models.TextChoices):
    NEW = "new", "New"
    PAID = "paid", "Paid"


class ExportRequestSerializer(serializers.Serializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Tags used to narrow the export.",
    )
    status = serializers.ChoiceField(
        choices=OrderStatus.choices,
        required=False,
        help_text="Optional order status filter.",
    )


class JobAcceptedSerializer(serializers.Serializer):
    job_id = serializers.UUIDField(
        help_text="Identifier used to query the background job status."
    )
    status = serializers.ChoiceField(
        choices=("queued",),
        help_text="Initial job state.",
    )
