from django.contrib import admin

from .models import UptimeCheck, UptimeStats, Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
        "status",
        "url",
        "check_interval",
        "timeout",
        "check_ssl",
        "check_performance",
        "check_security",
        "last_check",
    )
    search_fields = ("name", "url", "user__email")
    list_filter = ("status", "check_ssl", "check_performance", "check_security")


@admin.register(UptimeCheck)
class UptimeCheckAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "website",
        "uptime",
        "response_time",
        "status_code",
        "checked_at",
    )
    search_fields = ("website__name", "uptime")
    list_filter = ("uptime", "status_code")


@admin.register(UptimeStats)
class UptimeStatsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "website",
        "date",
        "uptime_percentage",
        "total_checks",
        "successful_checks",
        "average_response_time",
        "max_response_time",
        "min_response_time",
        "downtime_duration",
    )
    search_fields = ("website__name",)
    list_filter = ("date",)
