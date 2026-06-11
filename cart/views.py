from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Dish

from .cart import Cart
from .forms import CartAddForm, OrderForm
from .models import Order, OrderItem


@require_POST
def cart_add(request, dish_id):
    """Добавить блюдo в корзину."""
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id, is_available=True)
    form = CartAddForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(dish=dish, quantity=data["quantity"], override_quantity=data["override"])
        messages.success(request, f"«{dish.name}» добавлено в корзину.")
    return redirect(request.POST.get("next") or "cart:cart_detail")


@require_POST
def cart_remove(request, dish_id):
    """Удалить блюдо из корзины."""
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    cart.remove(dish)
    messages.info(request, f"«{dish.name}» удалено из корзины.")
    return redirect("cart:cart_detail")


def cart_detail(request):
    """Страница корзины."""
    cart = Cart(request)
    # Форма для изменения количества по каждой позиции
    for item in cart:
        item["update_form"] = CartAddForm(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(request, "cart/cart_detail.html", {"cart": cart})


@login_required
def order_list(request):
    """Список заказов текущего пользователя («Мои заказы»)."""
    orders = (
        request.user.orders
        .prefetch_related("items__dish")
        .all()
    )
    return render(request, "cart/order_list.html", {"orders": orders})


@login_required
def checkout(request):
    """Оформление заказа (доступно вошедшим пользователям)."""
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Корзина пуста.")
        return redirect("cart:cart_detail")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    dish=item["dish"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()
            return render(request, "cart/order_created.html", {"order": order})
    else:
        # Подставим имя пользователя по умолчанию
        form = OrderForm(initial={"full_name": request.user.get_full_name() or request.user.username})

    return render(request, "cart/checkout.html", {"cart": cart, "form": form})
