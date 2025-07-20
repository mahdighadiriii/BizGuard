import logging
import socket
from urllib.parse import urljoin, urlparse

import requests
from django.conf import settings
from django.utils import timezone
from rest_framework import status

from apps.monitoring.models import UptimeCheck, Website
from utils.choices import UpTimeStatusChoices

logger = logging.getLogger("monitoring")


class WebsiteMonitoringService:
    @staticmethod
    def _resolve_ip(url):
        hostname = urlparse(url).hostname
        return socket.gethostbyname(hostname) if hostname else None

    @staticmethod
    def _check_ssl(website, protocol, ip_address):
        if website.check_ssl and protocol != "https":
            logger.warning("SSL check enabled but URL is %s", protocol)
            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=UpTimeStatusChoices.ERROR,
                error_message="SSL check enabled but URL is not HTTPS",
                checked_at=timezone.now(),
                ip_address=ip_address,
            )
            return {
                "status": UpTimeStatusChoices.ERROR,
                "url": website.url,
                "details": {"message": "SSL check enabled but URL is not HTTPS"},
                "uptime_check_id": str(uptime_check.id),
                "ip_address": ip_address,
            }
        return None

    @staticmethod
    def _handle_response(website, response, context):
        status_code = response.status_code
        redirect_url = None
        if status_code in (301, 302):
            uptime_status = UpTimeStatusChoices.REDIRECT
            redirect_url = response.headers.get("Location")
            if redirect_url:
                redirect_url = urljoin(website.url, redirect_url)
            details = {
                "message": f"Redirect to {redirect_url}",
                "redirect_url": redirect_url,
            }
            if redirect_url:
                final_response = context["session"].get(
                    redirect_url,
                    timeout=context["timeout"],
                    headers=context["headers"],
                )
                status_code = final_response.status_code
                if status_code >= status.HTTP_400_BAD_REQUEST:
                    uptime_status = UpTimeStatusChoices.DOWN
                    details = {
                        "message": (f"Server Error {status_code} after redirect"),
                        "redirect_url": redirect_url,
                    }
        elif status_code == status.HTTP_200_OK:
            uptime_status = UpTimeStatusChoices.UP
            details = {"message": "The website is active."}
        elif status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            uptime_status = UpTimeStatusChoices.ERROR
            details = {"message": "Limit on the number of requests"}
        elif status_code >= status.HTTP_400_BAD_REQUEST:
            uptime_status = UpTimeStatusChoices.DOWN
            details = {"message": f"Server Error {status_code}"}
        else:
            uptime_status = UpTimeStatusChoices.ERROR
            details = {"message": f"Unknown Error! {status_code}"}
        return status_code, uptime_status, details, redirect_url

    @staticmethod
    def check_website_status(website: Website) -> dict:
        logger.info("Checking website: %s", website.url)
        try:
            ip_address = WebsiteMonitoringService._resolve_ip(website.url)
            protocol = urlparse(website.url).scheme
            ssl_result = WebsiteMonitoringService._check_ssl(
                website, protocol, ip_address
            )
            if ssl_result:
                return ssl_result

            timeout = min(website.timeout, 30)
            start_time = timezone.now()
            session = requests.Session()
            headers = {
                "User-Agent": "BizGuard-Monitoring/1.0",
                "Authorization": f"Basic {settings.MONITORING_AUTH_TOKEN}",
            }
            response = session.get(
                website.url,
                timeout=timeout,
                allow_redirects=False,
                headers=headers,
            )
            end_time = timezone.now()
            response_time = (end_time - start_time).total_seconds() * 1000

            context = {
                "session": session,
                "timeout": timeout,
                "headers": headers,
                "ip_address": ip_address,
            }
            status_code, uptime_status, details, redirect_url = (
                WebsiteMonitoringService._handle_response(website, response, context)
            )

            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=uptime_status,
                response_time=round(response_time, 2),
                status_code=status_code,
                headers=dict(response.headers),
                content_length=(len(response.content) if response.content else 0),
                checked_at=timezone.now(),
                error_message=details.get("message"),
                redirect_url=redirect_url,
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
                ip_address=ip_address,
            )
            return {
                "status": UpTimeStatusChoices.ERROR,
                "url": website.url,
                "details": {"message": f"DNS resolution failed: {e!s}"},
                "uptime_check_id": str(uptime_check.id),
                "ip_address": ip_address,
            }
        except requests.exceptions.Timeout:
            logger.exception("Timeout checking %s", website.url)
            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=UpTimeStatusChoices.TIMEOUT,
                error_message="Request expired",
                checked_at=timezone.now(),
                ip_address=ip_address,
            )
            return {
                "status": UpTimeStatusChoices.TIMEOUT,
                "url": website.url,
                "details": {"message": "Request expired"},
                "uptime_check_id": str(uptime_check.id),
                "ip_address": ip_address,
            }
        except requests.exceptions.ConnectionError:
            logger.exception("Connection error checking %s", website.url)
            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=UpTimeStatusChoices.DOWN,
                error_message="Unable to connect to the server",
                checked_at=timezone.now(),
                ip_address=ip_address,
            )
            return {
                "status": UpTimeStatusChoices.DOWN,
                "url": website.url,
                "details": {"message": "Unable to connect to the server"},
                "uptime_check_id": str(uptime_check.id),
                "ip_address": ip_address,
            }
        except Exception as e:
            logger.exception("Error checking %s", website.url)
            uptime_check = UptimeCheck.objects.create(
                website=website,
                uptime=UpTimeStatusChoices.ERROR,
                error_message=str(e),
                checked_at=timezone.now(),
                ip_address=ip_address,
            )
            return {
                "status": UpTimeStatusChoices.ERROR,
                "url": website.url,
                "details": {"message": str(e)},
                "uptime_check_id": str(uptime_check.id),
                "ip_address": ip_address,
            }
