import logging

import requests
from django.utils import timezone
from rest_framework import status

from apps.monitoring.models import UptimeCheck, Website
from utils.choices import UpTimeStatusChoices

logger = logging.getLogger("monitoring")


class WebsiteMonitoringService:
    @staticmethod
    def check_website_status(website: Website) -> dict:
        logger.info("Checking website: %s", website.url)
        try:
            timeout = min(website.timeout, 30)
            start_time = timezone.now()
            response = requests.get(
                website.url,
                timeout=timeout,
                allow_redirects=True,
                headers={"User-Agent": "BizGuard-Monitoring/1.0"},
            )
            end_time = timezone.now()
            response_time = (end_time - start_time).total_seconds() * 1000

            status_code = response.status_code
            if status_code == status.HTTP_200_OK:
                uptime_status = UpTimeStatusChoices.UP
                details = {"message": "The website is active."}
            elif status_code in (301, 302):
                status_code = UpTimeStatusChoices.REDIRECT
                details = {
                    "message": f"Redirect To{response.url}",
                    "redirect_url": response.url,
                }
            elif status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                uptime_status = UpTimeStatusChoices.ERROR
                details = {"message": "Limit on the number of requests"}
            elif status_code >= status.HTTP_400_BAD_REQUEST:
                uptime_status = UpTimeStatusChoices.DOWN
                details = {"message": f"Server Error {status_code}"}
            else:
                uptime_status = UpTimeStatusChoices.ERROR
                details = {"message": f"Unkown Error! {status_code}"}

            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=uptime_status,
                response_time=round(response_time, 2),
                status_code=status_code,
                headers=dict(response.headers),
                content_length=len(response.content),
                checked_at=timezone.timezone.now(),
                error_message=details.get("messsage"),
                redirect_url=details.get("redirect_url"),
                ip_address=response.raw.connection.sock.getpeername()[0]
                if response.raw.connection
                else None,
            )

            website.last_check = timezone.now()
            website.save(update_fields=["last_check"])

            logger.debug("Website %s status: %s", website.url, uptime_status)
            return {
                "status": uptime_status,
                "url": website.url,
                "response_time": round(response_time, 2),
                "status_code": status_code,
                "details": details,
                "uptime_check_id": str(uptime_check.id),
            }

        except requests.exceptions.Timeout:
            logger.exception("Timeout checking %s", website.url)
            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=UpTimeStatusChoices.TIMEOUT,
                error_message="Request expired",
                checked_at=timezone.timezone.now(),
            )
            return {
                "status": UpTimeStatusChoices.DOWN,
                "url": website.url,
                "details": {"message": "Unable to connect to the server."},
                "uptime_check_id": str(uptime_check.id),
            }
        except Exception as e:
            logger.exception("Error checking %s", website.url)
            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=UpTimeStatusChoices.ERROR,
                error_message=str(e),
                checked_at=timezone.now(),
            )
            return {
                "status": UpTimeStatusChoices.ERROR,
                "url": website.url,
                "details": {"message": str(e)},
                "uptime_check_id": str(uptime_check.id),
            }
