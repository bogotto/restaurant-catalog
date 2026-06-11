from django.contrib import admin

from .models import Category, Dish, Like, SupportMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "weight", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    list_editable = ("price", "is_available")
    fieldsets = (
        ("Основное", {
            "fields": ("category", "name", "description", "image",
                       "price", "weight", "is_available"),
        }),
        ("Пищевая ценность (КБЖУ на 100 г)", {
            "fields": ("calories", "proteins", "fats", "carbs"),
        }),
    )


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created", "is_processed")
    list_filter = ("is_processed", "created")
    search_fields = ("name", "email", "phone", "message")
    list_editable = ("is_processed",)
    readonly_fields = ("name", "email", "phone", "message", "created")
    fields = ("name", "email", "phone", "message", "created", "is_processed")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("dish", "user", "created")
    list_filter = ("created",)
    search_fields = ("dish__name", "user__username")
