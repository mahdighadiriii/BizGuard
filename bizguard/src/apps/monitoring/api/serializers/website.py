from rest_framework import serializers

from apps.monitoring.models import UptimeCheck, Website


class WebSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = [
            "id",
            "name",
            "url",
            "status" "check_interval",
            "timeout",
            "check_ssl",
            "last_check",
        ]


class UptimeCheckSerializer(serializers.ModelSerializer):
    website = WebSiteSerializer(read_only=True)

    class Meta:
        model = UptimeCheck
        fields = [
            "id",
            "website",
            "uptime",
            "response_time",
            "status_code",
            "error_message",
            "checked_at",
            "headers",
            "content_length",
            "redirect_url",
            "ip_address",
        ]
