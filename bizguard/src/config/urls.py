"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import URLPattern, URLResolver, include, path
from django_observability.metrics import metrics_view
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

_patterns = [
    path("admin/", admin.site.urls),
    path("metrics/", metrics_view, name="metrics"),
    path("accounts/", include("apps.accounts.urls")),
    path("api/monitoring/", include("apps.monitoring.api.urls")),
    path("security/", include("apps.security.urls")),
    path("alerts/", include("apps.alerts.urls")),
    path("telegram/", include("apps.telegram.urls")),
    path("analytics/", include("apps.analytics.urls")),
    path("payments/", include("apps.payments.urls")),
]

urlpatterns: list[URLPattern | URLResolver] = [
    path(settings.BASE_PATH, include(_patterns)),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path(
            f"{settings.BASE_PATH}api/schema/",
            SpectacularAPIView.as_view(),
            name="schema",
        ),
        path(
            f"{settings.BASE_PATH}api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            f"{settings.BASE_PATH}api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]
