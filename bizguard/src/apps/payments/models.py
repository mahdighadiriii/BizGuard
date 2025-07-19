from django.db import models

from apps.accounts.models import User
from utils.base_model import BaseModel
from utils.choices import PaymentChoices, SubscriptionChoices


class Subscription(BaseModel):
    """User subscription management"""

    plan = models.CharField(max_length=55, choices=SubscriptionChoices.choices)
    status = models.CharField(max_length=55, choices=PaymentChoices.choices)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscription"
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default=True)

    class Meta:
        db_table = "subscriptions"


class Payment(BaseModel):
    """Payment transaction records"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="IRR")
    status = models.CharField(max_length=55, choices=PaymentChoices.choices)

    # Payment gateway fields
    gateway = models.CharField(max_length=55, default="zarinpal")
    transaction_id = models.CharField(max_length=255, unique=True)
    gateway_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "payments"
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["transaction_id"]),
        ]
