import datetime

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from expenses.models import Expense
from tests.test_expenses.factories import ExpenseFactory
from user.models import User


def _csv_upload(text):
    """Wrap CSV text as an uploaded file."""
    return SimpleUploadedFile("expenses.csv", text.encode(), content_type="text/csv")


@pytest.mark.django_db
class TestExpenseCsv:
    """Assert expenses export to and import from CSV."""

    def setup_method(self):
        """Create an authenticated user and instantiate APIClient."""
        self.client = APIClient()
        self.user = User.objects.create(email="user@user.com")
        self.client.force_authenticate(user=self.user)

    def test_export_writes_own_expenses_in_pounds_oldest_first(self):
        """Export lists the user's expenses as CSV with costs in pounds."""
        ExpenseFactory.create(
            user=self.user,
            name="Rent",
            category="housing",
            cost=95000,
            date=datetime.datetime(2026, 9, 1, 9, 0, tzinfo=datetime.UTC),
        )
        ExpenseFactory.create(
            user=self.user,
            name="Bus",
            category="transport",
            cost=275,
            date=datetime.datetime(2026, 8, 30, 9, 0, tzinfo=datetime.UTC),
        )
        ExpenseFactory.create(name="Not mine")

        response = self.client.get("/expenses/export/")

        assert response.status_code == 200
        assert response["Content-Type"] == "text/csv"
        assert response.content.decode().splitlines() == [
            "date,name,category,cost",
            "2026-08-30,bus,transport,2.75",
            "2026-09-01,rent,housing,950.00",
        ]

    def test_export_respects_list_filters(self):
        """The same filters as the list narrow the export."""
        ExpenseFactory.create(user=self.user, category="transport")
        ExpenseFactory.create(user=self.user, category="groceries")

        response = self.client.get("/expenses/export/?category=transport")

        assert len(response.content.decode().splitlines()) == 2

    def test_import_creates_expenses_for_user(self):
        """Each valid row becomes an expense owned by the uploader."""
        upload = _csv_upload(
            "date,name,category,cost\n"
            "2026-09-14,Groceries,groceries,42.35\n"
            "2026-09-15,Gift,,£10\n"
        )

        response = self.client.post("/expenses/import/", {"file": upload})

        assert response.status_code == 201
        assert response.data == {"created": 2}
        imported_expenses = Expense.objects.filter(user=self.user).order_by("date")
        assert [
            (expense.name, expense.category, expense.cost)
            for expense in imported_expenses
        ] == [("groceries", "groceries", 4235), ("gift", "other", 1000)]

    def test_import_saves_nothing_if_any_row_is_invalid(self):
        """Errors are reported by row number and no rows are saved."""
        upload = _csv_upload(
            "date,name,category,cost\n"
            "2026-09-14,Groceries,groceries,42.35\n"
            "2026-09-15,Bus,spaceship,2.50\n"
            "2026-09-16,Coffee,eating_out,3.333\n"
        )

        response = self.client.post("/expenses/import/", {"file": upload})

        assert response.status_code == 400
        row_errors = response.json()["rows"]
        assert set(row_errors) == {"3", "4"}
        assert "category" in row_errors["3"]
        assert "cost" in row_errors["4"]
        assert not Expense.objects.exists()

    def test_import_requires_the_expected_columns(self):
        """A CSV without the expected header is rejected."""
        upload = _csv_upload("when,what,amount\n2026-09-14,Groceries,42.35\n")

        response = self.client.post("/expenses/import/", {"file": upload})

        assert response.status_code == 400
        assert "columns" in response.json()["rows"]["1"]

    def test_import_rejects_files_that_are_not_utf8(self):
        """A file in another encoding is a 400, not a server error."""
        latin1_csv = "date,name,category,cost\n2026-09-14,Caf\u00e9,eating_out,3.20\n"
        upload = SimpleUploadedFile(
            "expenses.csv", latin1_csv.encode("latin-1"), content_type="text/csv"
        )

        response = self.client.post("/expenses/import/", {"file": upload})

        assert response.status_code == 400
        assert "file" in response.data
        assert not Expense.objects.exists()

    def test_exported_csv_imports_back(self):
        """An export can be imported again unchanged."""
        ExpenseFactory.create_batch(3, user=self.user)
        exported_csv = self.client.get("/expenses/export/").content.decode()
        Expense.objects.all().delete()

        response = self.client.post(
            "/expenses/import/", {"file": _csv_upload(exported_csv)}
        )

        assert response.status_code == 201
        assert response.data == {"created": 3}
