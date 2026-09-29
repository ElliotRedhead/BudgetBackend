import datetime

import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from expenses.models import Expense, RecurringExpense
from user.models import User


@pytest.mark.django_db
class TestRecurringExpenses:
    """Assert recurring expenses are added to a month exactly once."""

    def setup_method(self):
        """Create an authenticated user with a monthly rent payment."""
        self.client = APIClient()
        self.base_url = "/recurring-expenses/"
        self.user = User.objects.create(email="user@user.com")
        self.client.force_authenticate(user=self.user)
        self.rent = RecurringExpense.objects.create(
            user=self.user, name="Rent", category="housing", cost=95000, day_of_month=1
        )

    def test_create_recurring_expense(self):
        """A recurring expense is created for the requesting user."""
        response = self.client.post(
            self.base_url,
            {"name": "Gym", "category": "leisure", "cost": 3000, "day_of_month": 5},
        )

        assert response.status_code == 201
        assert RecurringExpense.objects.get(id=response.data["id"]).user == self.user

    def test_day_of_month_is_capped_at_28(self):
        """Days that some months lack are rejected."""
        response = self.client.post(
            self.base_url, {"name": "Gym", "cost": 3000, "day_of_month": 29}
        )

        assert response.status_code == 400
        assert "day_of_month" in response.data

    def test_list_only_own_recurring_expenses(self):
        """Users only see their own recurring expenses."""
        RecurringExpense.objects.create(
            user=User.objects.create(email="other@user.com"),
            name="Other rent",
            cost=1,
            day_of_month=1,
        )

        response = self.client.get(self.base_url)

        assert [item["id"] for item in response.data["results"]] == [self.rent.id]

    def test_apply_adds_month_entries_once(self):
        """Applying twice for the same month only adds each expense once."""
        first_apply = self.client.post(f"{self.base_url}apply/?month=2026-09")
        second_apply = self.client.post(f"{self.base_url}apply/?month=2026-09")

        assert first_apply.status_code == 201
        assert len(first_apply.data["created"]) == 1
        assert second_apply.data["created"] == []
        rent_payment = Expense.objects.get(recurring_expense=self.rent)
        assert rent_payment.user == self.user
        assert rent_payment.cost == 95000
        assert rent_payment.date == datetime.datetime(
            2026, 9, 1, 12, tzinfo=datetime.UTC
        )

    def test_apply_skips_inactive_and_other_users(self):
        """Paused recurring expenses and other users' ones aren't applied."""
        RecurringExpense.objects.create(
            user=self.user, name="Old gym", cost=3000, day_of_month=5, active=False
        )
        RecurringExpense.objects.create(
            user=User.objects.create(email="other@user.com"),
            name="Other rent",
            cost=1,
            day_of_month=1,
        )

        response = self.client.post(f"{self.base_url}apply/?month=2026-09")

        assert [expense["name"] for expense in response.data["created"]] == ["rent"]

    def test_expense_link_to_recurring_expense_is_read_only(self):
        """An expense can't be attached to a recurring expense through the API."""
        response = self.client.post(
            "/expenses/",
            {"name": "Rent", "cost": 1, "recurring_expense": self.rent.id},
        )

        assert response.status_code == 201
        assert response.data["recurring_expense"] is None

    def test_command_applies_for_every_user(self):
        """The scheduled command applies every user's recurring expenses."""
        other_user_rent = RecurringExpense.objects.create(
            user=User.objects.create(email="other@user.com"),
            name="Other rent",
            cost=1,
            day_of_month=1,
        )

        call_command("apply_recurring_expenses", "--month", "2026-09")
        call_command("apply_recurring_expenses", "--month", "2026-09")

        assert Expense.objects.filter(recurring_expense=self.rent).count() == 1
        assert Expense.objects.filter(recurring_expense=other_user_rent).count() == 1
