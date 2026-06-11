from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категория меню (например, «Салаты», «Супы», «Десерты»)."""

    name = models.CharField("Название категории", max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Dish(models.Model):
    """Блюдо каталога с описанием, ценой, весом, фото и КБЖУ."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="dishes",
        verbose_name="Категория",
    )
    name = models.CharField("Название блюда", max_length=200)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    weight = models.PositiveIntegerField("Вес, г", blank=True, null=True)
    image = models.ImageField(
        "Фото", upload_to="dishes/", blank=True, null=True
    )
    is_available = models.BooleanField("В наличии", default=True)

    # --- КБЖУ (пищевая ценность на 100 г) ---------------------------------
    calories = models.PositiveIntegerField(
        "Калорийность, ккал", blank=True, null=True,
        help_text="На 100 г продукта",
    )
    proteins = models.DecimalField(
        "Белки, г", max_digits=5, decimal_places=1, blank=True, null=True,
        help_text="На 100 г продукта",
    )
    fats = models.DecimalField(
        "Жиры, г", max_digits=5, decimal_places=1, blank=True, null=True,
        help_text="На 100 г продукта",
    )
    carbs = models.DecimalField(
        "Углеводы, г", max_digits=5, decimal_places=1, blank=True, null=True,
        help_text="На 100 г продукта",
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ["category__name", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:dish_detail", args=[self.pk])

    @property
    def has_nutrition(self):
        """Заданы ли хотя бы какие-то данные КБЖУ."""
        return any(
            value is not None
            for value in (self.calories, self.proteins, self.fats, self.carbs)
        )

    @property
    def likes_count(self):
        return self.likes.count()


class Like(models.Model):
    """Лайк (оценка) блюда пользователем."""

    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="likes",
        verbose_name="Пользователь",
    )
    dish = models.ForeignKey(
        "Dish", on_delete=models.CASCADE, related_name="likes",
        verbose_name="Блюдо",
    )
    created = models.DateTimeField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        unique_together = ("user", "dish")  # один пользователь — один лайк

    def __str__(self):
        return f"{self.user} ♥ {self.dish}"


class SupportMessage(models.Model):
    """Обращение гостя в поддержку через форму обратной связи."""

    name = models.CharField("Имя", max_length=150)
    email = models.EmailField("E-mail")
    phone = models.CharField("Телефон", max_length=20, blank=True)
    message = models.TextField("Сообщение")
    created = models.DateTimeField("Получено", auto_now_add=True)
    is_processed = models.BooleanField("Обработано", default=False)

    class Meta:
        verbose_name = "Обращение в поддержку"
        verbose_name_plural = "Обращения в поддержку"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.name} ({self.created:%d.%m.%Y %H:%M})"
