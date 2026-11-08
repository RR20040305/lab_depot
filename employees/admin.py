from django.contrib import admin
from .models import Employee
from issues.models import Issue

class EmployeeIssueInline(admin.TabularInline):
    model = Issue
    fk_name = 'employee'
    fields = ("equipment", "return_date", "status")
    extra = 0
    can_delete = False

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("emp_id", "fio", "position", "lab")
    search_fields = ("fio", "emp_id")
    list_filter = ("lab",)
    ordering = ("fio",)
    inlines = (EmployeeIssueInline,)
