from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from expenses.models import Expense, RecurringExpense
from mixins import ExportCsvMixin


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ("export_as_csv",)
    list_display = ("name", "category", "user_link", "date")
    list_filter = ("category",)
    search_fields = ("name", "user__email")
    ordering = ("-date",)
    readonly_fields = ("user_link",)

    @admin.display(description="user")
    def user_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>'.format(
                reverse(
                    "admin:{}_{}_change".format(
                        obj.user._meta.app_label, obj.user._meta.model_name
                    ),
                    args=(obj.user.pk,),
                ),
                obj.user.email,
            )
        )


@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "day_of_month", "active", "user")
    list_filter = ("active", "category")
    search_fields = ("name", "user__email")
