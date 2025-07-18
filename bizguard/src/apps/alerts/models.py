import uuid

from django.db import models

from apps.accounts.models import User
from apps.monitoring.models import Website
from utils.base_model import BaseModel
from utils.choices import TriggerTypesChoices


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
