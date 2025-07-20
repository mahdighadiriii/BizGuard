import logging
import socket
from urllib.parse import urlparse

import requests
from django.conf import settings
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
            hostname = urlparse(website.url).hostname
            ip_address = socket.gethostbyname(hostname) if hostname else None

            timeout = min(website.timeout, 30)
            start_time = timezone.now()
            session = requests.session()
            response = requests.get(
                website.url,
                timeout=timeout,
                allow_redirects=False,
                headers={
                    "User-Agent": "BizGuard-Monitoring/1.0",
                    "Authorization": f"Basic {settings.MONITORING_AUTH_TOKEN}",
                },
            )
            end_time = timezone.now()
            response_time = (end_time - start_time).total_seconds() * 1000

            status_code = response.status_code
            if status_code == status.HTTP_200_OK:
                uptime_status = UpTimeStatusChoices.UP
                details = {"message": "The website is active."}
            elif status_code in (301, 302):
                uptime_status = UpTimeStatusChoices.REDIRECT
                redirect_url = response.headers.get("Location")
                details = {
                    "message": f"Redirect to {redirect_url}",
                    "redirect_url": redirect_url,
                }
                final_response = session.get(
                    redirect_url,
                    timeout=timeout,
                    headers={"User-Agent": "BizGuard-Monitoring/1.0"},
                )
                status_code = final_response.status_code

            elif status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                uptime_status = UpTimeStatusChoices.ERROR
                details = {"message": "Limit on the number of requests"}
            elif status_code >= status.HTTP_400_BAD_REQUEST:
                uptime_status = UpTimeStatusChoices.DOWN
                details = {"message": f"Server Error {status_code}"}
            else:
                uptime_status = UpTimeStatusChoices.ERROR
                details = {"message": f"Unknown Error! {status_code}"}

            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=uptime_status,
                response_time=round(response_time, 2),
                status_code=status_code,
                headers=dict(response.headers),
                content_length=len(response.content),
                checked_at=timezone.now(),
                error_message=details.get("message"),
                redirect_url=details.get("redirect_url"),
                ip_address=ip_address,
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
                "ip_address": ip_address,
            }

        except (socket.gaierror, ValueError) as e:
            logger.exception("DNS resolution failed for %s", website.url)
            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=UpTimeStatusChoices.ERROR,
                error_message=f"DNS resolution failed: {e!s}",
                checked_at=timezone.now(),
            )
            return {
                "status": UpTimeStatusChoices.ERROR,
                "url": website.url,
                "details": {"message": f"DNS resolution failed: {e!s}"},
                "uptime_check_id": str(uptime_check.id),
            }
        except requests.exceptions.Timeout:
            logger.exception("Timeout checking %s", website.url)
            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=UpTimeStatusChoices.TIMEOUT,
                error_message="Request expired",
                checked_at=timezone.now(),
            )
            return {
                "status": UpTimeStatusChoices.TIMEOUT,
                "url": website.url,
                "details": {"message": "Request expired"},
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
