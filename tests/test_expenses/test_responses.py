import json

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from snapshottest import TestCase

from tests.test_expenses.factories import ExpenseFactory


@pytest.mark.django_db
class TestExpenseResponses(TestCase):
    """Create and assert snapshot match on API JSON response structure."""

    def setUp(self):
        """Generate expense examples and instantiate APIClient."""
        self.client = APIClient()
        self.base_url = "/expenses/"
        self.admin = User.objects.create_superuser(username="admin")
        self.user = User.objects.create(username="user")

    def test_expense_list_response_admin(self):
        """Match response of retrieving all expenses as admin."""
        ExpenseFactory.create_batch(5)
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.base_url)

        assert response.status_code == 200
        assert len(response.data) == 5
        self.assertMatchSnapshot(json.loads(response.content))

    def test_expense_list_response_user(self):
        """Match response of retrieving all expenses for current user."""
        ExpenseFactory.create_batch(5)
        ExpenseFactory.create_batch(2, user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.base_url)

        assert response.status_code == 200
        assert len(response.data) == 2
        self.assertMatchSnapshot(json.loads(response.content))

    def test_expense_list_empty_response(self):
        """Match response of retrieving all expenses when none available."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.base_url)

        assert response.status_code == 200
        assert len(response.data) == 0
        self.assertMatchSnapshot(json.loads(response.content))

    def test_expense_detail_response_admin(self):
        """Match response of retrieving single expense as admin."""
        expenses = ExpenseFactory.create_batch(5)
        self.client.force_authenticate(user=self.admin)
        for expense_id in range(1, len(expenses) + 1):
            response = self.client.get(f"{self.base_url}{expense_id}/")
            assert response.status_code == 200
            self.assertMatchSnapshot(json.loads(response.content))

    def test_expense_detail_response_user_owned(self):
        """Match response of retrieving single expense as owning user."""
        expense = ExpenseFactory.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.base_url}{expense.id}/")
        assert response.status_code == 200
        assert len(response.data) > 0
        self.assertMatchSnapshot(json.loads(response.content))

    def test_expense_detail_response_not_user_owned(self):
        """Match response of retrieving single expense as non-owning user."""
        expense = ExpenseFactory.create()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.base_url}{expense.id}/")
        assert response.status_code == 404
