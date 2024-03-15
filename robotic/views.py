from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import RoboticUser
from .forms import RoboticLoginForm, RoboticRegisterForm
from django.db.models import Q


def index(request):
    user = request.user

    return render(request, 'robotic/pages/index.html', {
        'page_name': 'Home',
        'user': user,
    })

def account_not_active(request):
    user = request.user
    if user.is_authenticated:
        messages.error(request, 'Sua conta ainda não foi ativada por um administrador!')
        return redirect('robotic:index')

    return render(request, 'robotic/pages/account_not_active.html')


@login_required(login_url='robotic:login_student')
def root_page(request):
    user = request.user
    robotic_user = RoboticUser.objects.get(user=user)

    if not robotic_user.is_active:
        return redirect('robotic:logout')
    if robotic_user.role == "student":
        print(f'\n{robotic_user.role}\n')
        messages.error(request, 'Voce não tem permissão para acessar esta página. Você é Aluno!')
        return redirect('robotic:index')
    user_to_activate = RoboticUser.objects.all().exclude(id=robotic_user.id)
    return render(request, 'robotic/pages/root_page.html', {
        'user_to_activate': user_to_activate,

    })


def activate_user(request, id):
    user = request.user
    robotic_user = RoboticUser.objects.get(user=user)
    print(robotic_user.user.id)
    if not robotic_user.is_active:
        return redirect('robotic:logout')
    if robotic_user.role == "student":
        return JsonResponse({'message': 'You are not authorized to perform this action.'}, status=404)
    robotic_user = get_object_or_404(RoboticUser, id=id)

    print(robotic_user.user.username)

    if robotic_user:
        robotic_user.is_active = not robotic_user.is_active
        robotic_user.save()
        message = 'User has been activated' if robotic_user.is_active else 'User has been deactivated'
        return JsonResponse({'message': message}, status=200)
    else:
        return JsonResponse({'message': 'User not found.'}, status=404)


def login_page(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('robotic:index')
    if request.method == 'POST':
        form = RoboticLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Olá {user.username}!')
                    return redirect('robotic:index')
                else:
                    messages.error(request, 'Sua conta ainda não foi ativada por um administrador!')
                    return redirect('robotic:account_not_active')
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
                return redirect('robotic:login')
    else:
        form = RoboticLoginForm()
        return render(request, 'robotic/pages/login_page.html', {
            'form': form,
        })

def signup_page(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('robotic:index')
    if request.method == "POST":
        form = RoboticRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            level_access = form.cleaned_data['level_access']
            if password1 != password2:
                return redirect(reverse('chat:signup'))
            form.save()
            return redirect('robotic:index')
        else:
            return redirect('robotic:signup')
    else:
        form = RoboticRegisterForm()
        return render(request, 'robotic/pages/signup_page.html', {
            'form': form,
        })

def logout_page(request):
    logout(request)
    return redirect('robotic:index')