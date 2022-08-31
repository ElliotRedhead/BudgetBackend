from django_filters import rest_framework as filters

from expenses.models import Expense


class ExpenseFilterset(filters.FilterSet):
    """Filterset relevant to the Expense model."""

    date_range = filters.DateRangeFilter(field_name="date")
    _SCOPE_CHOICES = (("global", "Global"), ("self", "Self"))
    scope = filters.ChoiceFilter(
        label="Scope", choices=_SCOPE_CHOICES, method="user_scope"
    )

    def filter_queryset(self, queryset, filter_ownership=True):
        """Optionally filter expenses to the request user."""
        if filter_ownership:
            queryset = queryset.filter(user_id=self.request.user.id)
        return super().filter_queryset(queryset)

    def user_scope(self, queryset, _, param_value):
        """Only accessible by superuser, optionally scope to superuser."""
        match param_value:
            case "global":
                if (
                    self.request.user.is_superuser
                    and queryset.values("user").distinct().count() <= 1
                ):
                    return self.filter_queryset(self.queryset, False)
                else:
                    return queryset
            case "self":
                return queryset.filter(user_id=self.request.user.id)
            case "_":
                return queryset.filter(user_id=self.request.user.id)

    class Meta:
        """Define meta model and fields for filterset."""

        model = Expense
        fields = {
            "name": ["icontains"],
            "cost": ["lt", "gt"],
            "user": ["exact"],
        }
