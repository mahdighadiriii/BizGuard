import uuid

from django.db import models

from apps.monitoring.models import Website
from utils.base_model import BaseModel
from utils.choices import ScanTypesChoices, SeverityLevelsChoices


class SecurityScan(BaseModel):
    """Security scan results"""

    scan_types = models.CharField(max_length=30, choices=ScanTypesChoices.choices)
    severity_levels = models.CharField(
        max_length=30, choices=SeverityLevelsChoices.choices
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="security_scans"
    )
    title = models.CharField(max_length=95)
    is_resolved = models.BooleanField(default=False)  # type: ignore[assignment]
    scan_data = models.JSONField(default=dict)
    scanned_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_taable = "scurity_scans"
        indexes = [
            models.Index(fields=["website", "scan_type"]),
            models.Index(fields=["severity_levels", "is_resolved"]),
        ]


class SSLCertificates(BaseModel):
    """SSL certificates information"""

    website = models.OneToOneField(
        Website, on_delete=models.CASCADE, related_name="ssl_certificate"
    )
    issuer = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=95)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_valid = models.BooleanField(default=True)
    signature_algorithm = models.CharField(max_length=50)
    last_checked = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ssl_certificates"
