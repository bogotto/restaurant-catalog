from django import forms

from .models import SupportMessage


class SupportForm(forms.ModelForm):
    """Форма обратной связи на странице поддержки."""

    class Meta:
        model = SupportMessage
        fields = ("name", "email", "phone", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Как к вам обращаться"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+7 900 000-00-00 (по желанию)"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Опишите ваш вопрос или проблему"}),
        }
