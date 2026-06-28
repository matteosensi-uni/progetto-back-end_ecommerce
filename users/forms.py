from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "address",
            "phone",
        )


class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "address",
            "phone",
            )


class CustomAuthenticationForm(AuthenticationForm):
        
    def confirm_login_allowed(self, user):
            if not user.is_active:
                raise ValidationError("This account is inactive.")
