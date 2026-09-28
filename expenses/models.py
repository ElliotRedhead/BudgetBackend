from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now

from user.models import User


class LowercaseCharField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()


class Category(models.TextChoices):
    GROCERIES = "groceries", "Groceries"
    HOUSING = "housing", "Housing"
    UTILITIES = "utilities", "Utilities"
    TRANSPORT = "transport", "Transport"
    HEALTH = "health", "Health"
    EATING_OUT = "eating_out", "Eating out"
    LEISURE = "leisure", "Leisure"
    SHOPPING = "shopping", "Shopping"
    OTHER = "other", "Other"


class Expense(models.Model):
    name = LowercaseCharField(max_length=30, blank=False, null=False)
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.OTHER
    )
    cost = models.IntegerField(
        blank=False,
        null=False,
        help_text="Price of expense in smallest denomination. e.g. (£10 = 1000)",
        validators=[MinValueValidator(0)],
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(
        default=now, help_text="The date that the expense was conducted."
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
