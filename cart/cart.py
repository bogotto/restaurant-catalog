"""
Корзина на основе сессии.

Хранит товары в сессии пользователя, поэтому работает и для незарегистрированных
гостей, и для вошедших пользователей. Данные не теряются между страницами.
"""
from decimal import Decimal

from django.conf import settings

from catalog.models import Dish


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if cart is None:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, dish, quantity=1, override_quantity=False):
        """Добавить блюдо в корзину или изменить его количество."""
        dish_id = str(dish.id)
        if dish_id not in self.cart:
            self.cart[dish_id] = {"quantity": 0, "price": str(dish.price)}
        if override_quantity:
            self.cart[dish_id]["quantity"] = quantity
        else:
            self.cart[dish_id]["quantity"] += quantity
        self.save()

    def remove(self, dish):
        """Удалить блюдо из корзины."""
        dish_id = str(dish.id)
        if dish_id in self.cart:
            del self.cart[dish_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        """Перебрать блюда в корзине, подгрузив объекты из БД."""
        dish_ids = self.cart.keys()
        dishes = Dish.objects.filter(id__in=dish_ids)
        cart = self.cart.copy()
        for dish in dishes:
            cart[str(dish.id)]["dish"] = dish
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """Общее количество единиц товара в корзине."""
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """Итоговая стоимость всех товаров в корзине."""
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        """Очистить корзину."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
