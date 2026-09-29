import datetime

import pytest
from rest_framework.test import APIClient

from budgets.models import Budget
from tests.test_expenses.factories import ExpenseFactory
from user.models import User


def _in_month(year, month, day=15):
    """A timestamp in the middle of the given month."""
    return datetime.datetime(year, month, day, 12, 0, tzinfo=datetime.UTC)


@pytest.mark.django_db
class TestMonthlySummary:
    """Assert the monthly summary totals spending against the budget."""

    def setup_method(self):
        """Create an authenticated user and instantiate APIClient."""
        self.client = APIClient()
        self.url = "/expenses/summary/"
        self.user = User.objects.create(email="user@user.com")
        self.client.force_authenticate(user=self.user)

    def test_summary_totals_month_by_category(self):
        """Only the month's expenses count, grouped by category, largest first."""
        september = _in_month(2026, 9)
        ExpenseFactory.create(
            user=self.user, category="groceries", cost=3000, date=september
        )
        ExpenseFactory.create(
            user=self.user, category="groceries", cost=2000, date=september
        )
        ExpenseFactory.create(
            user=self.user, category="housing", cost=90000, date=september
        )
        ExpenseFactory.create(user=self.user, cost=7777, date=_in_month(2026, 8))
        ExpenseFactory.create(cost=5555, date=september)
        Budget.objects.create(
            user=self.user, month=datetime.date(2026, 9, 1), amount=200000
        )

        response = self.client.get(f"{self.url}?month=2026-09")

        assert response.status_code == 200
        assert response.data["month"] == "2026-09-01"
        assert response.data["total"] == 95000
        assert response.data["budget"] == 200000
        assert response.data["remaining"] == 105000
        assert response.data["by_category"] == [
            {"category": "housing", "total": 90000},
            {"category": "groceries", "total": 5000},
        ]

    def test_summary_carries_forward_latest_earlier_budget(self):
        """Without a budget for the month, the most recent earlier one applies."""
        Budget.objects.create(
            user=self.user, month=datetime.date(2026, 6, 1), amount=100000
        )
        Budget.objects.create(
            user=self.user, month=datetime.date(2026, 10, 1), amount=999
        )

        response = self.client.get(f"{self.url}?month=2026-09")

        assert response.data["budget"] == 100000
        assert response.data["budget_month"] == "2026-06-01"
        assert response.data["remaining"] == 100000

    def test_summary_without_budget_or_expenses(self):
        """An empty month has zero spent and no budget."""
        response = self.client.get(f"{self.url}?month=2026-09")

        assert response.data["total"] == 0
        assert response.data["budget"] is None
        assert response.data["remaining"] is None
        assert response.data["by_category"] == []

    def test_summary_rejects_malformed_month(self):
        """The month must be YYYY-MM."""
        response = self.client.get(f"{self.url}?month=September")

        assert response.status_code == 400
        assert "month" in response.data

    def test_summary_requires_authentication(self):
        """Anonymous users can't see a summary."""
        self.client.force_authenticate(user=None)

        assert self.client.get(self.url).status_code == 401
