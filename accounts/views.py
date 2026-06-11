from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import RegisterForm


def register(request):
    """Регистрация нового пользователя (гостя) с автоматическим входом."""
    if request.user.is_authenticated:
        return redirect("catalog:dish_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect("catalog:dish_list")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


class UserLoginView(LoginView):
    """Вход пользователя."""
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Выход пользователя."""
    next_page = reverse_lazy("catalog:dish_list")
