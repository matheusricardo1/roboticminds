from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import RoboticUser, Certificate


class CertificateCreateFrom(forms.Form):
    class Meta:
        model = Certificate
        fields = ('name', 'details', 'start_date', 'end_date', 'city', 'hours')


class RoboticLoginForm(forms.Form):
    username = forms.CharField(label="Nome de Usuário")
    password = forms.CharField(label="Senha", max_length=40, widget=forms.PasswordInput())


class RoboticRegisterForm(UserCreationForm):
    LEVEL_CHOICES = [
        ('teacher', 'Professor'),
        ('student', 'Aluno'),
    ]
   
    username = forms.CharField(label='Nome de Usuario:')
    #full_name = forms.CharField(label='Nome Completo:', max_length=200, widget=forms.TextInput())
    #email = forms.CharField(label='Email:', max_length=200, widget=forms.EmailInput())
    #cpf = forms.CharField(label='CPF:', min_length=11, max_length=11, widget=forms.TextInput())
    #registration = forms.CharField(label="Matrícula:", min_length=11, max_length=11, widget=forms.TextInput())
    password1 = forms.CharField(label='Senha:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme sua Senha:', widget=forms.PasswordInput)
    level_access = forms.ChoiceField(choices=LEVEL_CHOICES, label='Tipo de Usuário:', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = RoboticUser
        fields = [
            'username', 
            #'full_name', 
            #'email', 
            #'cpf', 
            #'registration', 
            'password1', 
            'password2',
        ]

class RoboticUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = RoboticUser
        fields = ('username', 'email')

class RoboticUserChangeForm(UserChangeForm):
    class Meta:
        model = RoboticUser
        fields = ('username', 'email')
