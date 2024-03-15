from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import RoboticUser


class RoboticLoginForm(forms.Form):
    email = forms.CharField(label="Email", min_length=11, max_length=11)
    password = forms.CharField(label="Senha", max_length=40, widget=forms.PasswordInput())


class RoboticRegisterForm(forms.Form):
    username = forms.CharField(label="Nome de Usuário", max_length=100, widget=forms.TextInput())
    fullname = forms.CharField(label="Nome Completo", max_length=200, widget=forms.TextInput())
    cpf = forms.CharField(label="CPF", min_length=11, max_length=11, widget=forms.TextInput())
    registration = forms.CharField(label="Matrícula", min_length=11, max_length=11, widget=forms.TextInput())
    email = forms.CharField(label="Email", max_length=200, widget=forms.EmailInput())
    password = forms.CharField(label="Senha", max_length=40, widget=forms.PasswordInput())


class RoboticUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = RoboticUser
        fields = ('username', 'email')

class RoboticUserChangeForm(UserChangeForm):
    class Meta:
        model = RoboticUser
        fields = ('username', 'email')
