from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_supportmessage"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Like",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="Дата")),
                ("dish", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="catalog.dish", verbose_name="Блюдо")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to=settings.AUTH_USER_MODEL, verbose_name="Пользователь")),
            ],
            options={
                "verbose_name": "Лайк",
                "verbose_name_plural": "Лайки",
                "unique_together": {("user", "dish")},
            },
        ),
    ]
