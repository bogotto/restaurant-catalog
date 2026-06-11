from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.dish_list, name="dish_list"),
    path("dish/<int:pk>/", views.dish_detail, name="dish_detail"),
    path("dish/<int:dish_id>/like/", views.toggle_like, name="toggle_like"),
    path("support/", views.support, name="support"),
]
