from django.db import models


class Laboratory(models.Model):
    lab_id = models.CharField(
        max_length=10, primary_key=True, verbose_name="Номер лаборатории"
    )
    responsible = models.CharField(
        max_length=100, verbose_name="Ответственный"
    )
    location = models.CharField(
        max_length=200, verbose_name="Расположение"
    )

    def __str__(self):
        return f"{self.lab_id} - {self.responsible}"

    class Meta:
        verbose_name = "Лаборатория"
        verbose_name_plural = "Лаборатории"
        ordering = ["lab_id"]
