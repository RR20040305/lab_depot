from django.db import models
from equipment.models import Equipment
from employees.models import Employee

class Issue(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активна"
        CANCELLED = "cancelled", "Отменена"
        COMPLETED = "completed", "Завершена"

    equipment = models.ForeignKey(
        Equipment, on_delete=models.PROTECT, related_name="issues", verbose_name="Оборудование"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, related_name="issues", verbose_name="Сотрудник"
    )
    return_date = models.DateField(verbose_name="Дата возврата")
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.ACTIVE, verbose_name="Статус"
    )

    def __str__(self):
        return f"Выдача №{self.pk}: {self.equipment.name} -> {self.employee.fio}"

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"
        ordering = ["-return_date"]
