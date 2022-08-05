from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from mixins import ExportCsvMixin

from expenses.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ("export_as_csv",)
    list_display = ("name", "user_link", "date")
    search_fields = ("name", "user__email")
    ordering = ("-date",)
    readonly_fields = ("user_link",)

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

    user_link.short_description = "user"
