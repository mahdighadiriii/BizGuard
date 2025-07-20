# src/apps/monitoring/views.py
import requests
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.monitoring.api.serializers import UptimeCheckSerializer
from apps.monitoring.models import UptimeCheck, Website


class WebsiteCheckView(APIView):
    serializer_class = UptimeCheckSerializer

    def get(self, request, website_id):
        try:
            website = Website.objects.get(id=website_id, user=request.user)
            response = requests.head(website.url, timeout=website.timeout)
            is_up = response.status_code == status.HTTP_200_OK
            uptime_status = "up" if is_up else "down"
            response_time = response.elapsed.total_seconds() * 1000

            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=uptime_status,
                response_time=response_time,
                status_code=response.status_code,
                checked_at=timezone.now(),
                headers=dict(response.headers),
                content_length=len(response.content) if response.content else None,
            )

            serializer = UptimeCheckSerializer(uptime_check)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Website.DoesNotExist:
            return Response(
                {"error": "وب‌سایت پیدا نشد"}, status=status.HTTP_404_NOT_FOUND
            )
        except requests.RequestException as e:
            UptimeCheck.objects.create(
                website=website,
                uptime="error",
                error_message=str(e),
                checked_at=timezone.now(),
            )
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
