import datetime

from expenses.models import Expense


def apply_recurring_expenses(recurring_expenses, month):
    """Create each active recurring expense's entry for the month, once only.

    Returns the expenses created. Running it again for the same month
    creates nothing, so it's safe to call from a scheduler or a button.
    """
    created_expenses = []
    for recurring_expense in recurring_expenses.filter(active=True):
        already_applied = recurring_expense.expenses.filter(
            date__year=month.year, date__month=month.month
        ).exists()
        if already_applied:
            continue
        created_expenses.append(
            Expense.objects.create(
                user=recurring_expense.user,
                name=recurring_expense.name,
                category=recurring_expense.category,
                cost=recurring_expense.cost,
                recurring_expense=recurring_expense,
                # Midday UTC keeps the date the same in UK time all year.
                date=datetime.datetime(
                    month.year,
                    month.month,
                    recurring_expense.day_of_month,
                    12,
                    tzinfo=datetime.UTC,
                ),
            )
        )
    return created_expenses
