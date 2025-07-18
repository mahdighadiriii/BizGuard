from django.contrib import admin

from .models import SecurityScan, SSLCertificates


@admin.register(SecurityScan)
class SecurityScanAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "website",
        "scan_types",
        "severity_levels",
        "title",
        "is_resolved",
        "scanned_at",
        "resolved_at",
    )
    search_fields = ("website__name", "title", "scan_types", "severity_levels")
    list_filter = ("scan_types", "severity_levels", "is_resolved")


@admin.register(SSLCertificates)
class SSLCertificatesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "website",
        "issuer",
        "subject",
        "serial_number",
        "valid_from",
        "valid_until",
        "is_valid",
        "signature_algorithm",
        "last_checked",
    )
    search_fields = ("website__name", "issuer", "subject", "serial_number")
    list_filter = ("is_valid", "valid_from", "valid_until")
