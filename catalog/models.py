from django.db import models


class Category(models.Model):
    name = models.CharField("Название категории", max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="dishes",
        verbose_name="Категория",
    )
    name = models.CharField("Название блюда", max_length=200)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена, ₽", max_digits=8, decimal_places=2)
    weight = models.PositiveIntegerField("Вес, г", blank=True, null=True)
    is_available = models.BooleanField("В наличии", default=True)

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self):
        return self.name