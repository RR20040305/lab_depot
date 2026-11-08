from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Equipment(models.Model):
    inv_num = models.CharField(
        max_length=20, 
        primary_key=True, 
        verbose_name="Инвентарный номер"
    )
    name = models.CharField(
        max_length=100, 
        verbose_name="Название",
        help_text="Укажите полное название оборудования"
    )
    status = models.CharField(
        max_length=50, 
        verbose_name="Состояние", 
        default="исправно"
    )
    
    slug = models.SlugField(
    max_length=150, 
    unique=True,  # Теперь можно
    blank=True, 
    editable=False, 
    verbose_name="URL-идентификатор"
    )

    def __str__(self):
        return f"{self.name} ({self.inv_num})"

    def get_absolute_url(self):
        return reverse("equipment:detail", kwargs={"inv_num": self.inv_num})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.inv_num}")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Оборудование"
        verbose_name_plural = "Оборудование"
        ordering = ["name"]
