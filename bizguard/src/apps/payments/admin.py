from django.contrib import admin

from .models import Payment, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "plan",
        "status",
        "start_date",
        "end_date",
        "auto_renew",
    )
    search_fields = ("user__username", "plan", "status")
    list_filter = ("plan", "status", "auto_renew")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "subscription",
        "amount",
        "currency",
        "status",
        "gateway",
        "transaction_id",
        "completed_at",
    )
    search_fields = ("user__username", "transaction_id", "gateway_transaction_id")
    list_filter = ("status", "gateway", "currency")
