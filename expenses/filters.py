from django_filters import rest_framework as filters

from expenses.models import Expense


class ExpenseFilterset(filters.FilterSet):
    """Filterset relevant to the Expense model."""

    date_range = filters.DateRangeFilter(field_name="date")

    def filter_queryset(self, queryset):
        """Queryset restricted to logged-in user only, unless superuser."""
        filtered_queryset = super().filter_queryset(queryset)
        if not self.request.user.is_superuser:
            filtered_queryset = filtered_queryset.filter(user=self.request.user)
        return filtered_queryset

    class Meta:
        """Define meta model and fields for filterset."""

        model = Expense
        fields = {
            "name": ["icontains"],
            "cost": ["lt", "gt"],
            "user": ["exact"],
        }
