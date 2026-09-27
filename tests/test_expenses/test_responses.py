import pytest
from rest_framework.test import APIClient

from expenses.models import Expense
from tests.test_expenses.factories import ExpenseFactory
from user.models import User


@pytest.mark.django_db
class TestExpenseResponses:
    """Assert expense list and detail responses are scoped to the right user."""

    def setup_method(self):
        """Create an admin and a regular user, and instantiate APIClient."""
        self.client = APIClient()
        self.base_url = "/expenses/"
        self.admin = User.objects.create_superuser(
            email="admin@admin.com", password="P4ssw0rd123!"
        )
        self.user = User.objects.create(email="user@user.com")

    def test_expense_list_response_admin(self):
        """An admin lists only their own expenses, even with the old scope param."""
        ExpenseFactory.create_batch(3)
        admin_expense = ExpenseFactory.create(user=self.admin)
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"{self.base_url}?scope=global")

        assert response.status_code == 200
        assert [expense["id"] for expense in response.data] == [admin_expense.id]

    def test_expense_list_response_user(self):
        """List only the requesting user's expenses, newest first."""
        ExpenseFactory.create_batch(5)
        user_expenses = ExpenseFactory.create_batch(2, user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.base_url)

        assert response.status_code == 200
        assert [expense["id"] for expense in response.data] == [
            expense.id for expense in reversed(user_expenses)
        ]

    def test_expense_list_empty_response(self):
        """Return an empty list when the user has no expenses."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.base_url)

        assert response.status_code == 200
        assert response.data == []

    def test_expense_detail_response_admin(self):
        """An admin can't retrieve another user's expense through the API."""
        other_user_expense = ExpenseFactory.create()
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            f"{self.base_url}{other_user_expense.id}/?scope=global"
        )

        assert response.status_code == 404

    def test_expense_delete_not_user_owned(self):
        """An admin can't delete another user's expense through the API."""
        other_user_expense = ExpenseFactory.create()
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(
            f"{self.base_url}{other_user_expense.id}/?scope=global"
        )

        assert response.status_code == 404
        assert Expense.objects.filter(id=other_user_expense.id).exists()

    def test_expense_detail_response_user_owned(self):
        """Return the owner's expense with a lowercased name and email as user."""
        user_expense = ExpenseFactory.create(
            user=self.user, name="Groceries", cost=4235
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.base_url}{user_expense.id}/")

        assert response.status_code == 200
        assert response.data["id"] == user_expense.id
        assert response.data["name"] == "groceries"
        assert response.data["cost"] == 4235
        assert response.data["user"] == "user@user.com"

    def test_expense_detail_response_not_user_owned(self):
        """Hide another user's expense behind a 404."""
        other_user_expense = ExpenseFactory.create()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.base_url}{other_user_expense.id}/")

        assert response.status_code == 404
