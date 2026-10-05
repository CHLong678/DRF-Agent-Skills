"""Large-table Django admin example.

Baseline: Django 3.2+.
"""

from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    show_full_result_count = False
    list_display = ("id", "name", "account", "owner", "created_at")
    list_select_related = ("account", "owner")
    autocomplete_fields = ("account", "owner")
    search_fields = ("id", "name")
    ordering = ("-created_at",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("account", "owner")
        )
