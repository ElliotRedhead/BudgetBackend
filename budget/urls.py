from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from expenses.urls import router as expenses_router

router = DefaultRouter()
router.registry.extend(expenses_router.registry)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
]
