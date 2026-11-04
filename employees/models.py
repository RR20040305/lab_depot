from django.db import models
from laboratories.models import Laboratory


class Employee(models.Model):
    emp_id = models.CharField(
        max_length=10, primary_key=True, verbose_name="Табельный номер"
    )
    fio = models.CharField(
        max_length=150, verbose_name="ФИО"
    )
    position = models.CharField(
        max_length=100, verbose_name="Должность"
    )
    lab = models.ForeignKey(
        Laboratory,
        on_delete=models.CASCADE,
        related_name="employees",
        verbose_name="Лаборатория"
    )

    def __str__(self):
        return f"{self.fio} ({self.position})"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["fio"]
