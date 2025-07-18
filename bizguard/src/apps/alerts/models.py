import uuid

from django.db import models

from apps.accounts.models import User
from apps.monitoring.models import Website
from utils.base_model import BaseModel
from utils.choices import AlertSeverityChoices, AlertStatusChoices, TriggerTypesChoices


class AlertRule(BaseModel):
    """Alert rule configuration"""

    trigger_types = models.CharField(max_length=35, choices=TriggerTypesChoices.choices)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alert_rules")
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="alert_rules"
    )
    threshold_value = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    cooldown_period = models.IntegerField(default=300)
    conditions = models.JSONField(default=dict)

    class Meta:
        db_table = "alert_rules"
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["website", "trigger_types"]),
        ]


class Alert(BaseModel):
    """Generated alerts"""

    alert_severity = models.CharField(
        max_length=55, choices=AlertSeverityChoices.choices
    )
    alert_status = models.CharField(max_length=55, choices=AlertStatusChoices.choices)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alerts")
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="alerts"
    )
    alert_rule = models.ForeignKey(
        AlertRule, on_delete=models.CASCADE, related_name="alerts"
    )

    title = models.CharField(max_length=100)
    message = models.TextField()

    sent_at = models.DateTimeField(null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    trigger_data = models.JSONField(default=dict)
    delivery_attempts = models.IntegerField(default=0)

    class Meta:
        db_table = "alerts"
        indexes = [
            models.Index(fields=["user", "alert_status"]),
            models.Index(fields=["website", "created_at"]),
            models.Index(fields=["alert_severity", "alert_status"]),
        ]
