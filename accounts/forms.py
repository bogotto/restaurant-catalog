from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """Форма регистрации гостя: имя пользователя, e-mail и пароль."""

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким e-mail уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
