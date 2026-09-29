from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import ExpenseViewSet, RecurringExpenseViewSet

router = DefaultRouter()
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(
    r"recurring-expenses", RecurringExpenseViewSet, basename="recurring-expense"
)

urlpatterns = [
    path(r"^", include(router.urls)),
]
