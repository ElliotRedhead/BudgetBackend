from django_filters import rest_framework as filters

from expenses.models import Expense


class ExpenseFilterset(filters.FilterSet):
    """Filterset relevant to the Expense model."""

    date_range = filters.DateRangeFilter(field_name="date")

    class Meta:
        """Define meta model and fields for filterset."""

        model = Expense
        fields = {
            "name": ["icontains"],
            "cost": ["lt", "gt"],
            "category": ["exact"],
        }
