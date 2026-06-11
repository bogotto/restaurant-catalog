from django import forms

from .models import Order


class CartAddForm(forms.Form):
    """Форма добавления блюда в корзину с выбором количества."""

    quantity = forms.IntegerField(
        min_value=1,
        max_value=50,
        initial=1,
        label="Количество",
        widget=forms.NumberInput(attrs={"class": "qty-input"}),
    )
    # Если True — заменить количество, иначе прибавить к текущему
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )


class OrderForm(forms.ModelForm):
    """Форма оформления заказа."""

    class Meta:
        model = Order
        fields = ("full_name", "phone", "address", "comment")
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Иван Иванов"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 900 000-00-00"}),
            "address": forms.TextInput(attrs={"placeholder": "Город, улица, дом, кв."}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Пожелания к заказу"}),
        }
