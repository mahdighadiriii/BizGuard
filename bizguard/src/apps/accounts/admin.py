from django.contrib import admin

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_superuser", "subscription_plan")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "business_name", "business_type", "alert_frequency")
    search_fields = ("user__email", "business_name")
    list_filter = ("alert_frequency",)
