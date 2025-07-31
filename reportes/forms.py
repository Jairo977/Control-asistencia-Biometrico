from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'rol', 'password1', 'password2')

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'rol', 'is_active', 'is_superuser')
