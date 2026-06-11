"""
Настройки проекта «Онлайн-каталог продукции ресторана».

Проект построен по трёхуровневой архитектуре (клиент — сервер приложений —
база данных) и разбит на модули-приложения:
    catalog  — каталог блюд (категории, блюда, КБЖУ, поиск);
    accounts — регистрация и вход пользователей (гостей);
    cart     — корзина и оформление заказа.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Безопасность -----------------------------------------------------------
# ВНИМАНИЕ: для реального развёртывания вынесите ключ в переменную окружения
# и установите DEBUG = False.
SECRET_KEY = "django-insecure-change-me-before-production-0123456789abcdef"

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", ".pythonanywhere.com"]

# --- Приложения -------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Приложения проекта
    "catalog",
    "accounts",
    "cart",
    "pages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "restaurant.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Делает корзину и категории доступными во всех шаблонах
                "cart.context_processors.cart",
                "catalog.context_processors.categories",
            ],
        },
    },
]

WSGI_APPLICATION = "restaurant.wsgi.application"

# --- База данных ------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Проверка паролей -------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Локализация ------------------------------------------------------------
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# --- Статика и медиа --------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Аутентификация ---------------------------------------------------------
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "catalog:dish_list"
LOGOUT_REDIRECT_URL = "catalog:dish_list"

# Идентификатор корзины в сессии
CART_SESSION_ID = "cart"
