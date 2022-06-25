from rest_framework.viewsets import ModelViewSet

from django_filters import rest_framework as filters
from expenses.filters import ExpenseFilterset

from expenses.models import Expense
from expenses.serializers import ExpenseSerializer


class ExpenseViewSet(ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all().order_by("-id")
    filterset_class = ExpenseFilterset

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
