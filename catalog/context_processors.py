"""Контекст-процессор: список категорий для меню навигации во всех шаблонах."""
from .models import Category


def categories(request):
    return {"nav_categories": Category.objects.all()}
