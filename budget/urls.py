from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from expenses.urls import router as expenses_router

router = DefaultRouter()
router.registry.extend(expenses_router.registry)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("schema/", SpectacularJSONAPIView.as_view(), name="schema"),
    path(
        "schema/swagger",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
