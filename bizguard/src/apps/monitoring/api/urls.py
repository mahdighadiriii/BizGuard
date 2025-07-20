from django.urls import path

from apps.monitoring.api.views.website import WebsiteCheckView

urlpatterns = [
    path("check/<uuid:website_id>/", WebsiteCheckView.as_view(), name="check-website"),
]
