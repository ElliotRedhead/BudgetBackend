from django.core.validators import MinValueValidator
from django.db import models

from user.models import User


class Budget(models.Model):
    """How much a user plans to spend in one calendar month."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    month = models.DateField(help_text="The first day of the month budgeted for.")
    amount = models.IntegerField(
        help_text="Budget in smallest denomination. e.g. (£10 = 1000)",
        validators=[MinValueValidator(0)],
    )

    class Meta:
        ordering = ["-month"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "month"], name="one_budget_per_user_per_month"
            )
        ]

    def __str__(self):
        return f"{self.month:%B %Y}: {self.amount}"
