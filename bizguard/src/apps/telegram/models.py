from django.db import models

from apps.accounts.models import User
from utils.base_model import BaseModel


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
