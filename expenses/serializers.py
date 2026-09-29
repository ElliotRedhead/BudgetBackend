from rest_framework import serializers

from expenses.models import Category, Expense


class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Expense
        fields = "__all__"


class CategoryTotalSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=Category.choices)
    total = serializers.IntegerField()


class MonthlySummarySerializer(serializers.Serializer):
    month = serializers.DateField(help_text="The first day of the month.")
    budget = serializers.IntegerField(
        allow_null=True,
        help_text="The month's budget, or the latest earlier one. Null if none set.",
    )
    budget_month = serializers.DateField(
        allow_null=True, help_text="The month the budget was set for."
    )
    total = serializers.IntegerField(help_text="Total spent in the month.")
    remaining = serializers.IntegerField(
        allow_null=True, help_text="Budget minus total. Null if no budget."
    )
    by_category = CategoryTotalSerializer(many=True)


class ExpenseImportSerializer(serializers.Serializer):
    file = serializers.FileField(
        help_text="CSV with columns date, name, category, cost (in pounds)."
    )


class ExpenseImportResultSerializer(serializers.Serializer):
    created = serializers.IntegerField()
