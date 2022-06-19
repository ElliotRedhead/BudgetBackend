from expenses.models import Expense
import factory
import pytz
import datetime

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
    cost = factory.Faker("pydecimal", min_value=0, max_value=1000)
    user = factory.SubFactory(UserFactory)
    date = factory.Faker(
        "date_time", tzinfo=pytz.UTC, end_datetime=datetime.date(2016, 5, 28)
    )
    date_created = factory.Faker("date_time", tzinfo=pytz.UTC)
    date_modified = factory.Faker("date_time", tzinfo=pytz.UTC)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        model_class.date_created.field.auto_now_add = False
        model_class.date_modified.field.auto_now = False

        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create(*args, **kwargs)

    class Meta:
        model = Expense
