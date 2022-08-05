from django.db import models
from django.utils.timezone import now

from user.models import User


class Expense(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    cost = models.IntegerField(
        blank=False,
        null=False,
        help_text="Price of expense in smallest denomination. e.g. (£10 = 1000)",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
