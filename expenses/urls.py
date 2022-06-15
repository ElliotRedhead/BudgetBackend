from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ExpenseViewSet

router = DefaultRouter()
router.register(r"expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    path(r"^", include(router.urls)),
]
