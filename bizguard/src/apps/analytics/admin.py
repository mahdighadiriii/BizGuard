from django.contrib import admin

from .models import AnomalyDetection, PerformanceMetric


@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ("id", "website", "metric_type", "value", "timestamp")
    list_filter = ("website", "metric_type")
    search_fields = ("website__name", "metric_type")
    readonly_fields = ("timestamp",)


@admin.register(AnomalyDetection)
class AnomalyDetectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "website",
        "anomaly_types",
        "confidence_score",
        "is_confirmed",
    )
    list_filter = ("website", "anomaly_types", "is_confirmed")
    search_fields = ("website__name", "anomaly_types")
