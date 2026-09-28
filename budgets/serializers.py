from rest_framework import serializers

from budgets.models import Budget


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ("id", "month", "amount")

    def validate_month(self, value):
        """Store any date in the month as the month's first day."""
        return value.replace(day=1)

    def validate(self, attrs):
        """Allow one budget per user per month."""
        month = attrs.get("month", getattr(self.instance, "month", None))
        existing_budgets = Budget.objects.filter(
            user=self.context["request"].user, month=month
        )
        if self.instance:
            existing_budgets = existing_budgets.exclude(id=self.instance.id)
        if existing_budgets.exists():
            raise serializers.ValidationError(
                {"month": "A budget for this month already exists."}
            )
        return attrs
