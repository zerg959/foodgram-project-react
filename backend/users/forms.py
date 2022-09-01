from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class PasswordChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',)
