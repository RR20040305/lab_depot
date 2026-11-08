from django.contrib import admin
from .models import Issue

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("id", "equipment", "employee", "return_date", "status")
    list_display_links = ("id",)
    search_fields = ("equipment__name", "employee__fio")  # Поиск по полям связанных моделей
    list_filter = ("status", "return_date")
    ordering = ("-return_date",)
    list_select_related = ("equipment", "employee")  # Оптимизация N+1 в админке
