from django.contrib import admin

from .models import AuditLog, SystemConfiguration


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "value",
        "created_at",
        "updated_at",
    )
    search_fields = ("key",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "action_type",
        "user",
        "resource_type",
        "resource_id",
        "ip_address",
        "timestamp",
    )
    search_fields = (
        "action_type",
        "user__username",
        "resource_type",
        "resource_id",
        "ip_address",
    )
    list_filter = (
        "action_type",
        "user",
        "resource_type",
        "timestamp",
    )

    readonly_fields = (
        "action_type",
        "user",
        "resource_type",
        "resource_id",
        "ip_address",
        "user_agent",
        "timestamp",
        "created_at",
        "updated_at",
        "is_active",
        "is_deleted",
        "description",
        "deleted_at",
        "deleted_by",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
