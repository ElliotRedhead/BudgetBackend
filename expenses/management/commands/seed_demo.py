import datetime
import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from budgets.models import Budget
from expenses.models import Expense, RecurringExpense
from expenses.recurring import apply_recurring_expenses
from user.models import User

DEMO_EMAIL = "demo@example.com"

# (name, category, lowest cost, highest cost in pence, times per month)
_DAY_TO_DAY_SPENDING = [
    ("Groceries", "groceries", 2500, 9000, 6),
    ("Coffee", "eating_out", 280, 450, 8),
    ("Takeaway", "eating_out", 1800, 3500, 2),
    ("Train ticket", "transport", 1200, 4800, 3),
    ("Fuel", "transport", 5000, 7000, 1),
    ("Cinema", "leisure", 1100, 2400, 1),
    ("Clothes", "shopping", 2000, 8000, 1),
    ("Pharmacy", "health", 400, 1800, 1),
]

_RECURRING = [
    ("Rent", "housing", 95000, 1),
    ("Energy", "utilities", 11500, 3),
    ("Broadband", "utilities", 3200, 12),
    ("Phone", "utilities", 1500, 18),
    ("Gym", "leisure", 3500, 25),
]


class Command(BaseCommand):
    help = "Create or reset a demo account with three months of expenses."

    def add_arguments(self, parser):
        parser.add_argument("--password", default="demo-budget-2026")

    def handle(self, *args, **options):
        User.objects.filter(email=DEMO_EMAIL).delete()
        demo_user = User.objects.create_user(
            email=DEMO_EMAIL, password=options["password"]
        )
        today = timezone.localdate()
        this_month = today.replace(day=1)
        months = [
            (this_month - datetime.timedelta(days=62)).replace(day=1),
            (this_month - datetime.timedelta(days=31)).replace(day=1),
            this_month,
        ]
        Budget.objects.create(user=demo_user, month=months[0], amount=180000)
        Budget.objects.create(user=demo_user, month=months[2], amount=200000)
        for name, category, cost, day_of_month in _RECURRING:
            RecurringExpense.objects.create(
                user=demo_user,
                name=name,
                category=category,
                cost=cost,
                day_of_month=day_of_month,
            )

        # A fixed seed gives the same demo data every time.
        rng = random.Random(2026)
        for month in months:
            apply_recurring_expenses(demo_user.recurring_expenses.all(), month)
            last_day = today.day if month == this_month else 28
            for name, category, low, high, times in _DAY_TO_DAY_SPENDING:
                for _ in range(times):
                    Expense.objects.create(
                        user=demo_user,
                        name=name,
                        category=category,
                        cost=rng.randint(low, high),
                        date=datetime.datetime(
                            month.year,
                            month.month,
                            rng.randint(1, last_day),
                            rng.randint(8, 20),
                            tzinfo=datetime.UTC,
                        ),
                    )

        self.stdout.write(
            f"Demo account {DEMO_EMAIL} ready with "
            f"{demo_user.expense_set.count()} expenses."
        )
