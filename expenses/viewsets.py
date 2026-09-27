from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from expenses.filters import ExpenseFilterset
from expenses.models import Expense
from expenses.serializers import ExpenseSerializer


class ExpenseViewSet(ModelViewSet):
    """Viewset definition related to Expense model."""

    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilterset

    def get_queryset(self):
        """Limit every action to the requesting user's expenses."""
        if getattr(self, "swagger_fake_view", False):
            return Expense.objects.none()
        return Expense.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        """Insert current user for related field on POST."""
        return serializer.save(user=self.request.user)
