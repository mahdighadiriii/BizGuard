from django.contrib import admin

from .models import Alert, AlertRule


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "website",
        "trigger_type",
        "threshold_value",
        "is_active",
        "cooldown_period",
    )
    list_filter = ("is_active", "trigger_type", "website", "user")
    search_fields = ("id", "user__username", "website__name")
    ordering = ("-created_at",)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "website",
        "alert_rule",
        "alert_severity",
        "alert_status",
        "title",
        "sent_at",
        "acknowledged_at",
        "resolved_at",
    )
    list_filter = ("alert_severity", "alert_status", "website", "user")
    search_fields = ("id", "user__username", "website__name", "title")
    ordering = ("-created_at",)
