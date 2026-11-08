from django.contrib import admin
from .models import Laboratory

@admin.register(Laboratory)
class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ("lab_id", "responsible", "location")
    search_fields = ("lab_id", "responsible", "location")
    ordering = ("lab_id",)
