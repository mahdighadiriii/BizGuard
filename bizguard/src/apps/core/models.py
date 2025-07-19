from django.db import models

from apps.accounts.models import User
from utils.base_model import BaseModel
from utils.choices import CoreActionChoices


class SystemConfiguration(BaseModel):
    """System-wide configuration"""

    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    class Meta:
        db_table = "system_configurations"


class AuditLog(BaseModel):
    """System audit log"""

    action_type = models.CharField(max_length=55, choices=CoreActionChoices.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    resource_type = models.CharField(max_length=55)
    resource_id = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_log"
        indexes = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["action_type", "timestamp"]),
        ]
