from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from budgets.models import Budget
from budgets.serializers import BudgetSerializer


class BudgetViewSet(ModelViewSet):
    """Monthly budgets belonging to the requesting user."""

    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer
    filterset_fields = ["month"]

    def get_queryset(self):
        """Limit every action to the requesting user's budgets."""
        if getattr(self, "swagger_fake_view", False):
            return Budget.objects.none()
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Insert current user for related field on POST."""
        return serializer.save(user=self.request.user)
