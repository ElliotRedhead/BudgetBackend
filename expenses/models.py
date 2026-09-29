from django.core.validators import MaxValueValidator, MinValueValidator
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


class RecurringExpense(models.Model):
    """An expense that repeats every month on the same day, e.g. rent."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recurring_expenses"
    )
    name = LowercaseCharField(max_length=30)
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.OTHER
    )
    cost = models.IntegerField(
        help_text="Price of expense in smallest denomination. e.g. (£10 = 1000)",
        validators=[MinValueValidator(0)],
    )
    day_of_month = models.PositiveSmallIntegerField(
        help_text="Day the expense is due. Capped at 28 so every month has it.",
        validators=[MinValueValidator(1), MaxValueValidator(28)],
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} on day {self.day_of_month}"


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
    recurring_expense = models.ForeignKey(
        RecurringExpense,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
        help_text="The recurring expense this was created from, if any.",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
