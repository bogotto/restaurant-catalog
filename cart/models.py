from django.contrib.auth.models import User
from django.db import models

from catalog.models import Dish


class Order(models.Model):
    """Заказ пользователя (реализация перспективной сущности из ТЗ)."""

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Пользователь",
    )
    full_name = models.CharField("Имя получателя", max_length=150)
    phone = models.CharField("Телефон", max_length=20)
    address = models.CharField("Адрес доставки", max_length=250)
    comment = models.TextField("Комментарий", blank=True)
    created = models.DateTimeField("Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created"]

    def __str__(self):
        return f"Заказ №{self.pk}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Позиция заказа: блюдо, его цена на момент заказа и количество."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ",
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_items",
        verbose_name="Блюдо",
    )
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.dish} × {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity
