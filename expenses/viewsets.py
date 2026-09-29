import datetime

from django.db.models import Sum
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from budgets.models import Budget
from expenses.filters import ExpenseFilterset
from expenses.models import Expense
from expenses.serializers import ExpenseSerializer, MonthlySummarySerializer


def _parse_month(value):
    """Turn "YYYY-MM" into the first day of that month, defaulting to now."""
    if value is None:
        return timezone.localdate().replace(day=1)
    try:
        return datetime.datetime.strptime(value, "%Y-%m").date()
    except ValueError as error:
        raise ValidationError({"month": "Use the format YYYY-MM."}) from error


class ExpenseViewSet(ModelViewSet):
    """Viewset definition related to Expense model."""

    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilterset

    def get_queryset(self):
        """Limit every action to the requesting user's expenses."""
        if getattr(self, "swagger_fake_view", False):
            return Expense.objects.none()
        return (
            Expense.objects.filter(user=self.request.user)
            .select_related("user")
            .order_by("-id")
        )

    def perform_create(self, serializer):
        """Insert current user for related field on POST."""
        return serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "month", str, description="YYYY-MM. Defaults to the current month."
            )
        ],
        responses=MonthlySummarySerializer,
    )
    @action(detail=False, pagination_class=None, filterset_class=None)
    def summary(self, request):
        """Total spending for a month against its budget, split by category."""
        month = _parse_month(request.query_params.get("month"))
        month_expenses = self.get_queryset().filter(
            date__year=month.year, date__month=month.month
        )
        total = month_expenses.aggregate(total=Sum("cost"))["total"] or 0
        by_category = (
            month_expenses.order_by()
            .values("category")
            .annotate(total=Sum("cost"))
            .order_by("-total", "category")
        )
        budget = (
            Budget.objects.filter(user=request.user, month__lte=month)
            .order_by("-month")
            .first()
        )
        summary = {
            "month": month,
            "budget": budget.amount if budget else None,
            "budget_month": budget.month if budget else None,
            "total": total,
            "remaining": budget.amount - total if budget else None,
            "by_category": list(by_category),
        }
        return Response(MonthlySummarySerializer(summary).data)
