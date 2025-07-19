from django.contrib import admin

from .models import TelegramMessages, TelegramSession


@admin.register(TelegramSession)
class TelegramSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "chat_id", "current_state", "last_interaction")
    search_fields = ("user__username", "chat_id", "current_state")
    readonly_fields = ("last_interaction",)


@admin.register(TelegramMessages)
class TelegramMessagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "message_type",
        "is_delivered",
        "created_at",
        "telegram_message_id",
    )
    search_fields = ("user__username", "message_type", "content", "telegram_message_id")
    list_filter = ("message_type", "is_delivered", "created_at")
    readonly_fields = ("created_at", "updated_at")
