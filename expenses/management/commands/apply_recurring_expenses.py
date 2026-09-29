from django.core.management.base import BaseCommand, CommandError
from rest_framework.exceptions import ValidationError

from expenses.models import RecurringExpense
from expenses.recurring import apply_recurring_expenses
from expenses.viewsets import parse_month


class Command(BaseCommand):
    help = "Create a month's entries for every user's recurring expenses."

    def add_arguments(self, parser):
        parser.add_argument("--month", help="YYYY-MM. Defaults to this month.")

    def handle(self, *args, **options):
        try:
            month = parse_month(options["month"])
        except ValidationError as error:
            raise CommandError("Use the format YYYY-MM for --month.") from error
        created_expenses = apply_recurring_expenses(
            RecurringExpense.objects.all(), month
        )
        self.stdout.write(
            f"Created {len(created_expenses)} expenses for {month:%B %Y}."
        )
