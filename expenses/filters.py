from django_filters import rest_framework as filters

from expenses.models import Expense


class ExpenseFilterset(filters.FilterSet):
    """Filterset relevant to the Expense model."""

    date_range = filters.DateRangeFilter(field_name="date")
    month = filters.DateFilter(
        method="filter_month",
        input_formats=["%Y-%m"],
        label="Month (YYYY-MM)",
    )

    def filter_month(self, queryset, name, value):
        """Keep expenses dated in the given calendar month."""
        return queryset.filter(date__year=value.year, date__month=value.month)

    class Meta:
        """Define meta model and fields for filterset."""

        model = Expense
        fields = {
            "name": ["icontains"],
            "cost": ["lt", "gt"],
            "category": ["exact"],
        }
