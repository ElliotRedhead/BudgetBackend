import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from user.models import User


@pytest.mark.django_db
def test_seed_demo_creates_a_usable_account_and_resets_on_rerun():
    """The demo account can log in, has data, and reseeding replaces it."""
    call_command("seed_demo", "--password", "Demo-P4ssword")
    first_expense_count = User.objects.get(email="demo@example.com").expense_set.count()
    call_command("seed_demo", "--password", "Demo-P4ssword")

    demo_user = User.objects.get(email="demo@example.com")
    login_response = APIClient().post(
        "/user/login/", {"email": "demo@example.com", "password": "Demo-P4ssword"}
    )

    assert login_response.status_code == 200
    assert demo_user.expense_set.count() == first_expense_count > 0
    assert demo_user.budgets.exists()
    assert demo_user.recurring_expenses.count() == 5
