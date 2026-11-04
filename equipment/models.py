from django.db import models


class Equipment(models.Model):
    inv_num = models.CharField(
        max_length=10, primary_key=True, verbose_name="Инвентарный номер"
    )
    name = models.CharField(
        max_length=100, verbose_name="Название"
    )
    status = models.CharField(
        max_length=50, verbose_name="Состояние", default="исправно"
    )

    def __str__(self):
        return f"{self.name} ({self.inv_num})"

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ["name"]
