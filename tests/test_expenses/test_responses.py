import json

import pytest
from rest_framework.test import APIClient

from tests.test_expenses.factories import ExpenseFactory


@pytest.mark.django_db
class TestExpenseResponses:
    def setup(self):
        ExpenseFactory.create_batch(5)

    def test_expense_list_response(self, snapshot):
        client = APIClient()
        response = client.get("/expenses/")

        assert response.status_code == 200
        snapshot.assert_match(json.loads(response.content))
