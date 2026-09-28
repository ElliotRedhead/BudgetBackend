import datetime

import pytest
from rest_framework.test import APIClient

from budgets.models import Budget
from user.models import User


@pytest.mark.django_db
class TestBudgets:
    """Assert monthly budgets are per user and one per month."""

    def setup_method(self):
        """Create an authenticated user and instantiate APIClient."""
        self.client = APIClient()
        self.base_url = "/budgets/"
        self.user = User.objects.create(email="user@user.com")
        self.client.force_authenticate(user=self.user)

    def test_create_budget_normalises_month_to_first_day(self):
        """Any date in the month is stored as the first of that month."""
        response = self.client.post(
            self.base_url, {"month": "2026-09-17", "amount": 200000}
        )

        assert response.status_code == 201
        assert response.data["month"] == "2026-09-01"
        created_budget = Budget.objects.get(id=response.data["id"])
        assert created_budget.user == self.user

    def test_second_budget_for_same_month_is_rejected(self):
        """A month can only have one budget per user."""
        Budget.objects.create(
            user=self.user, month=datetime.date(2026, 9, 1), amount=100
        )
        response = self.client.post(
            self.base_url, {"month": "2026-09-30", "amount": 200}
        )

        assert response.status_code == 400
        assert "month" in response.data

    def test_same_month_is_allowed_for_different_users(self):
        """Another user's budget doesn't block this user's month."""
        other_user = User.objects.create(email="other@user.com")
        Budget.objects.create(
            user=other_user, month=datetime.date(2026, 9, 1), amount=100
        )
        response = self.client.post(
            self.base_url, {"month": "2026-09-01", "amount": 200}
        )

        assert response.status_code == 201

    def test_update_budget_amount(self):
        """The amount can be changed without tripping the one-per-month rule."""
        user_budget = Budget.objects.create(
            user=self.user, month=datetime.date(2026, 9, 1), amount=100
        )
        response = self.client.patch(
            f"{self.base_url}{user_budget.id}/", {"amount": 150000}
        )

        assert response.status_code == 200
        user_budget.refresh_from_db()
        assert user_budget.amount == 150000

    def test_list_only_own_budgets_filtered_by_month(self):
        """Users see only their budgets, optionally for one month."""
        september_budget = Budget.objects.create(
            user=self.user, month=datetime.date(2026, 9, 1), amount=100
        )
        Budget.objects.create(
            user=self.user, month=datetime.date(2026, 8, 1), amount=100
        )
        Budget.objects.create(
            user=User.objects.create(email="other@user.com"),
            month=datetime.date(2026, 9, 1),
            amount=100,
        )
        response = self.client.get(f"{self.base_url}?month=2026-09-01")

        assert [budget["id"] for budget in response.data["results"]] == [
            september_budget.id
        ]

    def test_negative_budget_is_rejected(self):
        """A budget can't be negative."""
        response = self.client.post(
            self.base_url, {"month": "2026-09-01", "amount": -1}
        )

        assert response.status_code == 400
        assert "amount" in response.data
