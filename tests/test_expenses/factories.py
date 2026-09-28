import datetime

import factory

from expenses.models import Category, Expense
from tests.test_budget.factories import UserFactory

_EXPENSE_NAME_CHOICES = (
    "Groceries",
    "Healthcare",
    "Clothes",
    "Transport",
    "Utilities",
    "Furniture",
    "Leisure",
    "Holiday",
)


class ExpenseFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("random_element", elements=_EXPENSE_NAME_CHOICES)
    category = factory.Faker("random_element", elements=Category.values)
    cost = factory.Faker("pyint", min_value=0, max_value=100000)
    user = factory.SubFactory(UserFactory)
    date = factory.Faker(
        "date_time", tzinfo=datetime.UTC, end_datetime=datetime.date(2016, 5, 28)
    )
    date_created = factory.Faker("date_time", tzinfo=datetime.UTC)
    date_modified = factory.Faker("date_time", tzinfo=datetime.UTC)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Save the generated timestamps, then restore auto_now behaviour."""
        model_class.date_created.field.auto_now_add = False
        model_class.date_modified.field.auto_now = False
        try:
            if cls._meta.django_get_or_create:
                return cls._get_or_create(model_class, *args, **kwargs)

            manager = cls._get_manager(model_class)
            return manager.create(*args, **kwargs)
        finally:
            model_class.date_created.field.auto_now_add = True
            model_class.date_modified.field.auto_now = True

    class Meta:
        model = Expense
