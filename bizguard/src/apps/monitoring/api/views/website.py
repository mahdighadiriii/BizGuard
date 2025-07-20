# src/apps/monitoring/api/views/website.py
import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.monitoring.api.serializers.website import UptimeCheckSerializer
from apps.monitoring.api.services.monitoring import WebsiteMonitoringService
from apps.monitoring.models import UptimeCheck, Website

logger = logging.getLogger("monitoring")


class WebsiteCheckView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UptimeCheckSerializer

    def post(self, request, website_id):
        logger.info(
            "User %s requested check for website %s", request.user.id, website_id
        )
        try:
            website = Website.objects.get(id=website_id, user=request.user)
            result = WebsiteMonitoringService.check_website_status(website)
            serializer = self.serializer_class(
                UptimeCheck.objects.get(id=result["uptime_check_id"])
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Website.DoesNotExist:
            logger.exception(
                "Website %s not found for user %s",
                website_id,
                request.user.id,
            )
            return Response(
                {"error": "Website not found!"}, status=status.HTTP_404_NOT_FOUND
            )
