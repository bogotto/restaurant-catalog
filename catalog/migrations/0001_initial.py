from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="Название категории")),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Dish",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, verbose_name="Название блюда")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("price", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Цена")),
                ("weight", models.PositiveIntegerField(blank=True, null=True, verbose_name="Вес, г")),
                ("image", models.ImageField(blank=True, null=True, upload_to="dishes/", verbose_name="Фото")),
                ("is_available", models.BooleanField(default=True, verbose_name="В наличии")),
                ("calories", models.PositiveIntegerField(blank=True, help_text="На 100 г продукта", null=True, verbose_name="Калорийность, ккал")),
                ("proteins", models.DecimalField(blank=True, decimal_places=1, help_text="На 100 г продукта", max_digits=5, null=True, verbose_name="Белки, г")),
                ("fats", models.DecimalField(blank=True, decimal_places=1, help_text="На 100 г продукта", max_digits=5, null=True, verbose_name="Жиры, г")),
                ("carbs", models.DecimalField(blank=True, decimal_places=1, help_text="На 100 г продукта", max_digits=5, null=True, verbose_name="Углеводы, г")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="dishes", to="catalog.category", verbose_name="Категория")),
            ],
            options={
                "verbose_name": "Блюдо",
                "verbose_name_plural": "Блюда",
                "ordering": ["category__name", "name"],
            },
        ),
    ]
