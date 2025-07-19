from django.db import models

from apps.accounts.models import User
from utils.base_model import BaseModel
from utils.choices import TelegramMessageTypesChoices


class TelegramSession(BaseModel):
    """Telegram bot session management"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="telegram_session"
    )
    chat_id = models.BigIntegerField(unique=True)
    current_state = models.CharField(max_length=50, default="idle")
    context_data = models.JSONField(default=dict)
    last_interaction = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "telegram_sessions"


class TelegramMessages(BaseModel):
    """Telegram message log"""

    message_type = models.CharField(
        max_length=55, choices=TelegramMessageTypesChoices.choices
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="telegram_messages"
    )
    content = models.TextField()
    telegram_message_id = models.PositiveBigIntegerField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)

    class Meta:
        db_table = "telegram_messages"
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["message_type", "is_delivered"]),
        ]
