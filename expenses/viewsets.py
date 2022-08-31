from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from expenses.filters import ExpenseFilterset
from expenses.models import Expense
from expenses.serializers import ExpenseSerializer


class ExpenseViewSet(ModelViewSet):
    """Viewset definition related to Expense model."""

    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilterset
    queryset = Expense.objects.all().order_by("-id")

    def perform_create(self, serializer):
        """Insert current user for related field on POST."""
        return serializer.save(user=self.request.user)
