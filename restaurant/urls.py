"""Корневая маршрутизация проекта."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),
    path("accounts/", include("accounts.urls")),
    path("cart/", include("cart.urls")),
    path("", include("pages.urls")),
]

# Раздача загруженных изображений блюд во время разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
