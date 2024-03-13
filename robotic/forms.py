from django.forms import ModelForm
from robotic.models import RoboticUser
from django import forms


class LoginRoboticForm(forms.Form):
    cpf = forms.CharField(label="CPF", min_length=11, max_length=11)
    password = forms.CharField(label="Senha", max_length=40, widget=forms.PasswordInput())


class RegisterRoboticForm(forms.Form):
    username = forms.CharField(label="Nome de Usuário", max_length=100, widget=forms.TextInput())
    fullname = forms.CharField(label="Nome Completo", max_length=200, widget=forms.TextInput())
    cpf = forms.CharField(label="CPF", min_length=11, max_length=11, widget=forms.TextInput())
    email = forms.CharField(label="Email", max_length=200, widget=forms.EmailInput())
    password = forms.CharField(label="Senha", max_length=40, widget=forms.PasswordInput())
