from django.contrib import admin
from .models import Equipment
from issues.models import Issue

class EquipmentIssueInline(admin.TabularInline):
    model = Issue
    fk_name = 'equipment'
    fields = ("employee", "return_date", "status")
    extra = 0
    can_delete = False

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("inv_num", "name", "status", "slug")
    list_display_links = ("name",)
    list_editable = ("status",)  # Редактирование статуса прямо в списке
    search_fields = ("name", "inv_num")
    list_filter = ("status",)
    ordering = ("name",)
    readonly_fields = ("slug",)
    inlines = (EquipmentIssueInline,)
    view_on_site = True  # Ссылка "Посмотреть на сайте"
