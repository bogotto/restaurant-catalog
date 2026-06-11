from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("catalog", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=150, verbose_name="Имя получателя")),
                ("phone", models.CharField(max_length=20, verbose_name="Телефон")),
                ("address", models.CharField(max_length=250, verbose_name="Адрес доставки")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий")),
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="Создан")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to=settings.AUTH_USER_MODEL, verbose_name="Пользователь")),
            ],
            options={
                "verbose_name": "Заказ",
                "verbose_name_plural": "Заказы",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Цена")),
                ("quantity", models.PositiveIntegerField(default=1, verbose_name="Количество")),
                ("dish", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="order_items", to="catalog.dish", verbose_name="Блюдо")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="cart.order", verbose_name="Заказ")),
            ],
            options={
                "verbose_name": "Позиция заказа",
                "verbose_name_plural": "Позиции заказа",
            },
        ),
    ]
