from django.db import models


class PlanChoices(models.TextChoices):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class PlanFeatures(models.TextChoices):
    USER_LIMIT = "user_limit"
    STORAGE_LIMIT = "storage_limit"
    FEATURE_LIMIT = "feature_limit"


class PlanStatus(models.TextChoices):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


class PlanType(models.TextChoices):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PlanDuration(models.TextChoices):
    MONTH = "month"
    YEAR = "year"


class PlanCurrency(models.TextChoices):
    INR = "INR"
    USD = "USD"
