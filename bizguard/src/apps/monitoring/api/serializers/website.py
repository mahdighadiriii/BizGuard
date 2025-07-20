from rest_framework import serializers

from apps.monitoring.models import UptimeCheck


class UptimeCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = UptimeCheck
        fields = [
            "id",
            "uptime",
            "response_time",
            "status_code",
            "error_message",
            "checked_at",
        ]
