import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from bizguard.src.utils.choices import PlanChoices

from utils.base_model import BaseModel


class User(AbstractUser, BaseModel):
    choices = PlanChoices.choices
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    telegram_user_id = models.CharField(max_length=255, blank=True, null=True)
    telegram_username = models.CharField(max_length=255, blank=True, null=True)
    phonenumber = models.CharField(
        max_length=15,
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")],
    )
    subscription_plan = models.CharField(
        max_length=20,
        choices=PlanChoices.choices,
        default=PlanChoices.FREE,
    )
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    max_websites = models.IntegerField(default=1)  # type: ignore[assignment]
    max_checks_per_minute = models.IntegerField(default=1)  # type: ignore[assignment]
    is_telegram_verified = models.BooleanField(default=False)  # type: ignore[assignment]
    timezone = models.CharField(max_length=50, default="Asia/Tehran")

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["telegram_user_id"]),
            models.Index(fields=["subscription_plan"]),
        ]


class UserProfile(BaseModel):
    """Additional User Profile Info"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    business_name = models.CharField(max_length=200, null=True, blank=True)
    business_type = models.CharField(max_length=100, null=True, blank=True)
    notification_preferences = models.JSONField(default=dict)
    alert_frequency = models.CharField(
        max_length=20,
        choices=[
            ("immediate", "Immediate"),
            ("hourly", "Hourly"),
            ("daily", "Daily"),
        ],
        default="immediate",
    )

    class Meta:
        db_table = "user_profiles"
