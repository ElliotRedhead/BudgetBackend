import csv
import datetime
import io

from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from budgets.models import Budget
from expenses.csv_io import MAX_IMPORT_BYTES, parse_expenses_csv, write_expenses_csv
from expenses.filters import ExpenseFilterset
from expenses.models import Expense, RecurringExpense
from expenses.recurring import apply_recurring_expenses
from expenses.serializers import (
    AppliedRecurringExpensesSerializer,
    ExpenseImportResultSerializer,
    ExpenseImportSerializer,
    ExpenseSerializer,
    MonthlySummarySerializer,
    RecurringExpenseSerializer,
)


def parse_month(value):
    """Turn "YYYY-MM" into the first day of that month, defaulting to now."""
    if value is None:
        return timezone.localdate().replace(day=1)
    try:
        return datetime.datetime.strptime(value, "%Y-%m").date()
    except ValueError as error:
        raise ValidationError({"month": "Use the format YYYY-MM."}) from error


_MONTH_PARAMETER = OpenApiParameter(
    "month", str, description="YYYY-MM. Defaults to the current month."
)


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
            .order_by("-date", "-id")
        )

    def perform_create(self, serializer):
        """Insert current user for related field on POST."""
        return serializer.save(user=self.request.user)

    @extend_schema(parameters=[_MONTH_PARAMETER], responses=MonthlySummarySerializer)
    @action(detail=False, pagination_class=None, filterset_class=None)
    def summary(self, request):
        """Total spending for a month against its budget, split by category."""
        month = parse_month(request.query_params.get("month"))
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

    @extend_schema(responses={(200, "text/csv"): OpenApiTypes.STR})
    @action(detail=False, pagination_class=None)
    def export(self, request):
        """Download the (optionally filtered) expenses as CSV, oldest first."""
        expenses = self.filter_queryset(self.get_queryset()).order_by("date", "id")
        csv_text = io.StringIO()
        write_expenses_csv(expenses, csv_text)
        response = HttpResponse(csv_text.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="expenses.csv"'
        return response

    @extend_schema(
        request=ExpenseImportSerializer,
        responses={201: ExpenseImportResultSerializer},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="import",
        parser_classes=[MultiPartParser],
    )
    def import_csv(self, request):
        """Create expenses from a CSV upload. Nothing is saved if any row fails."""
        upload_serializer = ExpenseImportSerializer(data=request.data)
        upload_serializer.is_valid(raise_exception=True)
        uploaded_file = upload_serializer.validated_data["file"]
        if uploaded_file.size > MAX_IMPORT_BYTES:
            raise ValidationError({"file": "The file must be 1 MB or smaller."})

        try:
            row_serializers, row_errors = parse_expenses_csv(uploaded_file.file)
        except (UnicodeDecodeError, csv.Error) as error:
            raise ValidationError(
                {"file": "Upload a CSV file saved as UTF-8."}
            ) from error
        if row_errors:
            raise ValidationError({"rows": row_errors})
        with transaction.atomic():
            for row_serializer in row_serializers:
                row_serializer.save(user=request.user)
        return Response({"created": len(row_serializers)}, status=201)


class RecurringExpenseViewSet(ModelViewSet):
    """Monthly repeating expenses belonging to the requesting user."""

    permission_classes = [IsAuthenticated]
    serializer_class = RecurringExpenseSerializer

    def get_queryset(self):
        """Limit every action to the requesting user's recurring expenses."""
        if getattr(self, "swagger_fake_view", False):
            return RecurringExpense.objects.none()
        return RecurringExpense.objects.filter(user=self.request.user).order_by(
            "day_of_month", "id"
        )

    def perform_create(self, serializer):
        """Insert current user for related field on POST."""
        return serializer.save(user=self.request.user)

    @extend_schema(
        request=None,
        parameters=[_MONTH_PARAMETER],
        responses={201: AppliedRecurringExpensesSerializer},
    )
    @action(detail=False, methods=["post"])
    def apply(self, request):
        """Add the month's recurring expenses that haven't been added yet."""
        month = parse_month(request.query_params.get("month"))
        created_expenses = apply_recurring_expenses(self.get_queryset(), month)
        return Response(
            AppliedRecurringExpensesSerializer({"created": created_expenses}).data,
            status=201,
        )
