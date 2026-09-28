from rest_framework.routers import DefaultRouter

from .viewsets import BudgetViewSet

router = DefaultRouter()
router.register(r"budgets", BudgetViewSet, basename="budget")
