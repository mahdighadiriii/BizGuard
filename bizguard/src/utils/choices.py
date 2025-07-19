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


class StatusChoices(models.TextChoices):
    ACTIVE = "active"
    PAUSED = "paused"
    DELETED = "deleted"


class UpTimeStatusChoices(models.TextChoices):
    UP = "up"
    DOWN = "down"
    ERROR = "error"
    TIMEOUT = "timeout"


class ScanTypesChoices(models.TextChoices):
    SSL = "ssl"
    VULNERABILITY = "vulnerability"
    MALWARE = "malware"
    BLACKLIST = "blacklist"


class SeverityLevelsChoices(models.TextChoices):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TriggerTypesChoices(models.TextChoices):
    DOWNTIME = "Website Down"
    RESPONSE_TIME = "High Response Time"
    SSL_EXPIRY = "SSL Certificate Expiry"
    SECURITY_ISSUE = "Security Issue Detected"
    ANOMALY = "Anomaly Detected"


class AlertSeverityChoices(models.TextChoices):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertStatusChoices(models.TextChoices):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class TelegramMessageTypesChoices(models.TextChoices):
    INCOMING = "incoming"
    OUTGOING = "outgoing"
    COMMAND = "command"
    ALERT = "alert"


class MetricTypeChoices(models.TextChoices):
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    AVAILABILITY = "availability"


class AnomalyTypeChoices(models.TextChoices):
    RESPONSE_TIME = "Response Time Anomaly"
    TRAFFIC_PATTERN = "Traffic Pattern Anomaly"
    ERROR_SPIKE = "Error Spike"
    SECURITY_THREAT = "Security Threat"


class SubscriptionChoices(models.TextChoices):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"


class PaymentChoices(models.TextChoices):
    PENDING = "pending"
    COMPELETED = "compeleted"
    FAILED = "failed"
    REFUNDED = "refunded"


class CoreActionChoices(models.TextChoices):
    CREATED = "created"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    PAYMENT = "payment"
    ALERT = "alert"
