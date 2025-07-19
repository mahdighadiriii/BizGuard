from django.db import models

from apps.monitoring.models import Website
from utils.base_model import BaseModel
from utils.choices import AnomalyTypeChoices, MetricTypeChoices


class PerformanceMetric(BaseModel):
    """Performance metrics collection"""

    metric_type = models.CharField(max_length=55, choices=MetricTypeChoices.choices)
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="performance_metrics"
    )
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        db_table = "performance_metrics"
        indexes = [models.Index(fields=["website", "metric_type"])]


class AnomalyDetection(BaseModel):
    """Anomaly detection results"""

    anomaly_types = models.CharField(max_length=55, choices=AnomalyTypeChoices.choices)
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="anomalies"
    )
    confidence_score = models.FloatField()
    is_confirmed = models.BooleanField(default=False)
    anomaly_data = models.JSONField(default=dict)

    class Meta:
        db_table = "anomaly_detections"
        indexes = [
            models.Index(fields=["website", "detected_at"]),
            models.Index(fields=["anomaly_type", "confidence_score"]),
        ]
