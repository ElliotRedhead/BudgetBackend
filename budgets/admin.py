from django.contrib import admin

from budgets.models import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("month", "amount", "user")
    search_fields = ("user__email",)
    ordering = ("-month",)
