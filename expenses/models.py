from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Expense(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    cost = models.DecimalField(decimal_places=2, max_digits=19, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
