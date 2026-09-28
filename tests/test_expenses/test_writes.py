import pytest
from rest_framework.test import APIClient

from expenses.models import Expense
from tests.test_expenses.factories import ExpenseFactory
from user.models import User


@pytest.mark.django_db
class TestExpenseWrites:
    """Assert expenses can be created, updated and deleted by their owner."""

    def setup_method(self):
        """Create an authenticated user and instantiate APIClient."""
        self.client = APIClient()
        self.base_url = "/expenses/"
        self.user = User.objects.create(email="user@user.com")
        self.client.force_authenticate(user=self.user)

    def test_create_expense_for_requesting_user(self):
        """A new expense belongs to the requesting user, whatever is posted."""
        other_user = User.objects.create(email="other@user.com")
        response = self.client.post(
            self.base_url,
            {"name": "Rent", "cost": 95000, "user": other_user.id},
        )

        assert response.status_code == 201
        created_expense = Expense.objects.get(id=response.data["id"])
        assert created_expense.user == self.user
        assert created_expense.name == "rent"
        assert created_expense.cost == 95000

    def test_create_expense_rejects_fractional_cost(self):
        """Cost must be whole pence."""
        response = self.client.post(self.base_url, {"name": "Rent", "cost": "1.5"})

        assert response.status_code == 400
        assert "cost" in response.data

    def test_create_expense_rejects_negative_cost(self):
        """Cost can't be negative."""
        response = self.client.post(self.base_url, {"name": "Refund", "cost": -500})

        assert response.status_code == 400
        assert "cost" in response.data
        assert not Expense.objects.exists()

    def test_create_expense_accepts_zero_cost(self):
        """A free item can be recorded with zero cost."""
        response = self.client.post(self.base_url, {"name": "Sample", "cost": 0})

        assert response.status_code == 201

    def test_create_expense_requires_authentication(self):
        """Anonymous users can't create expenses."""
        self.client.force_authenticate(user=None)
        response = self.client.post(self.base_url, {"name": "Rent", "cost": 100})

        assert response.status_code == 401
        assert not Expense.objects.exists()

    def test_update_own_expense(self):
        """The owner can partially update an expense."""
        user_expense = ExpenseFactory.create(user=self.user, cost=100)
        response = self.client.patch(
            f"{self.base_url}{user_expense.id}/", {"cost": 250}
        )

        assert response.status_code == 200
        user_expense.refresh_from_db()
        assert user_expense.cost == 250

    def test_update_other_users_expense_is_not_found(self):
        """Another user's expense can't be updated."""
        other_user_expense = ExpenseFactory.create(cost=100)
        response = self.client.patch(
            f"{self.base_url}{other_user_expense.id}/", {"cost": 250}
        )

        assert response.status_code == 404
        other_user_expense.refresh_from_db()
        assert other_user_expense.cost == 100

    def test_delete_own_expense(self):
        """The owner can delete an expense."""
        user_expense = ExpenseFactory.create(user=self.user)
        response = self.client.delete(f"{self.base_url}{user_expense.id}/")

        assert response.status_code == 204
        assert not Expense.objects.filter(id=user_expense.id).exists()
