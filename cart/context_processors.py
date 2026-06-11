"""Контекст-процессор корзины: делает корзину доступной во всех шаблонах."""
from .cart import Cart


def cart(request):
    return {"cart": Cart(request)}
