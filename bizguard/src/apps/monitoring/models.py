import uuid

from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from django.db import models

from utils.base_model import BaseModel
from utils.choices import StatusChoices, UpTimeStatusChoices

User = get_user_model()


class Website(BaseModel):
    """Website monitoring configuration"""

    status = models.CharField(max_length=20, choices=StatusChoices)
    id = models.UUIDField(primaray=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="website")
    name = models.CharField(max_length=95)
    url = models.URLField(validators=[URLValidator()])
    check_interval = models.IntegerField(default=300)
    timeout = models.IntegerField(default=30)

    # Monitoring settings
    check_ssl = models.BooleanField(default=True)
    check_performance = models.BooleanField(default=True)

    # Premium feature
    check_security = models.BooleanField(default=True)

    # Metadata
    last_check = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "website"
        unique_together = ["user", "url"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["status", "last_check"]),
        ]


class UptimeCheck(BaseModel):
    """Indivisual uptime check status"""

    uptime = models.CharField(max_length=20, choices=UpTimeStatusChoices)
    id = models.UUIDField(primaray=True, default=uuid.uuid4, editable=False)
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="uptime_checks"
    )
    response_time = models.FloatField(null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    # Additional metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    headers = models.JSONField(default=dict)
    content_length = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "uptime_checks"
        indexes = [
            models.Index(fields=["website", "checked_at"]),
            models.Index(fields=["status", "checked_at"]),
        ]


class UptimeStats(BaseModel):
    """Aggregated uptime statistics"""

    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="stats")
    date = models.DateField()
    uptime_percentage = models.FloatField()
    total_checks = models.IntegerField()
    successful_checks = models.IntegerField()
    average_response_time = models.FloatField()
    max_response_time = models.FloatField()
    min_response_time = models.FloatField()
    downtime_duration = models.IntegerField(default=0)

    class Meta:
        db_table = "uptime_stats"
        unique_together = ["website", "date"]
        indexes = [models.Index(fields=["website", "date"])]
