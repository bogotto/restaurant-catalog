from django.shortcuts import render, get_object_or_404
from .models import Category, Dish


def dish_list(request):
    categories = Category.objects.all()
    dishes = Dish.objects.filter(is_available=True)
    return render(request, "catalog/dish_list.html", {
        "categories": categories,
        "dishes": dishes,
    })


def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    return render(request, "catalog/dish_detail.html", {"dish": dish})