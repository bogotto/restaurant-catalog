from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SupportForm
from .models import Category, Dish, Like


def dish_list(request):
    """Витрина каталога: список блюд с поиском, фильтром и лайками."""
    dishes = (
        Dish.objects.filter(is_available=True)
        .select_related("category")
        .annotate(likes_total=Count("likes"))
    )

    # Поиск по сайту: по названию и описанию блюда
    query = request.GET.get("q", "").strip()
    if query:
        dishes = dishes.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Фильтр по категории (передаётся id категории)
    category_id = request.GET.get("category")
    current_category = None
    if category_id:
        current_category = Category.objects.filter(pk=category_id).first()
        if current_category:
            dishes = dishes.filter(category=current_category)

    # Множество id блюд, которые лайкнул текущий пользователь
    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(request.user.likes.values_list("dish_id", flat=True))

    context = {
        "dishes": dishes,
        "query": query,
        "current_category": current_category,
        "liked_ids": liked_ids,
    }
    return render(request, "catalog/dish_list.html", context)


def dish_detail(request, pk):
    """Карточка блюда с подробным описанием, КБЖУ и лайком."""
    dish = get_object_or_404(Dish.objects.select_related("category"), pk=pk)
    liked = (
        request.user.is_authenticated
        and dish.likes.filter(user=request.user).exists()
    )
    return render(request, "catalog/dish_detail.html", {"dish": dish, "liked": liked})


@login_required
@require_POST
def toggle_like(request, dish_id):
    """Поставить или убрать лайк блюду (один пользователь — один лайк)."""
    dish = get_object_or_404(Dish, id=dish_id)
    like, created = Like.objects.get_or_create(user=request.user, dish=dish)
    if not created:
        like.delete()
    return redirect(request.POST.get("next") or dish.get_absolute_url())


def support(request):
    """Страница поддержки: контакты и форма обратной связи."""
    if request.method == "POST":
        form = SupportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Спасибо! Ваше обращение отправлено — мы свяжемся с вами в ближайшее время.",
            )
            return redirect("catalog:support")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "name": request.user.get_full_name() or request.user.username,
                "email": request.user.email,
            }
        form = SupportForm(initial=initial)

    return render(request, "catalog/support.html", {"form": form})
