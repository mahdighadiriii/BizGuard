from django.db import models


class PlanChoices(models.TextChoices):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class PlanFeaturesChoices(models.TextChoices):
    USER_LIMIT = "user_limit"
    STORAGE_LIMIT = "storage_limit"
    FEATURE_LIMIT = "feature_limit"


class PlanStatusChoices(models.TextChoices):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


class PlanTypeChoices(models.TextChoices):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PlanDurationChoices(models.TextChoices):
    MONTH = "month"
    YEAR = "year"


class PlanCurrencyChoices(models.TextChoices):
    INR = "INR"
    USD = "USD"


class AlertFrequencyChoices(models.TextChoices):
    IMMEDIATE = "immediate"
    HOURLY = "hourly"
    DAILY = "daily"
