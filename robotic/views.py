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


def login_student(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('robotic:index')
    if request.method == 'POST':
        form = RoboticLoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            password = form.cleaned_data['password']
            user_robotic = RoboticUser.objects.filter(cpf=cpf).first()
            if user_robotic is not None:
                if user_robotic.role == "teacher":
                    messages.error(request, 'Você tentou com Login de Aluno, mas você é Professor!')
                    return redirect('robotic:login_teacher')
                print(f'Nome do RoboticUser: {user_robotic.user.username}')
                is_active = user_robotic.is_active
                if not is_active:
                    messages.error(request, 'Sua conta ainda não foi ativada por um administrador!')
                    return redirect('robotic:account_not_active')
                else:
                    print(f'Nome do User: {user_robotic.user.username}\nSenha: {password}\n')
                    auth_user = authenticate(username=user_robotic.user.username, password=password)
                    print(auth_user)

                    if auth_user is not None:
                        login(request, auth_user)
                        messages.success(request, f'Olá {user_robotic.user.username}!')
                        return redirect('robotic:index')
            else:
                messages.error(request, 'Cpf ou senha inválidos.')
                return redirect('robotic:login_student')
    else:
        form = RoboticLoginForm()
        return render(request, 'robotic/pages/login_student.html', {
            'page_name': 'Aluno',
            'form': form,
        })


def login_teacher(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('robotic:index')
    if request.method == 'POST':
        form = RoboticLoginForm(request.POST)
        if form.is_valid():
            cpf = form.cleaned_data['cpf']
            password = form.cleaned_data['password']
            user_robotic = RoboticUser.objects.get(cpf=cpf)
            if user_robotic is not None:
                if user_robotic.role == "student":
                    messages.error(request, 'Você tentou com Login de Professor, mas você é Aluno!')
                    return redirect('robotic:login_student')
                is_active = user_robotic.is_active
                if not is_active:
                    messages.error(request, 'Sua conta ainda não foi ativada por um administrador!')
                    return redirect('robotic:account_not_active')
                else:
                    auth_user = authenticate(username=user_robotic.user.username, password=password)
                    if auth_user is not None:
                        login(request, auth_user)
                        messages.success(request, f'Olá {user_robotic.user.username}!')
                        return redirect('robotic:index')
            else:
                messages.error(request, 'Cpf ou senha inválidos.')
                return redirect('robotic:login_teacher')
    else:
        form = RoboticLoginForm()
    return render(request, 'robotic/pages/login_teacher.html', {
        'page_name': 'Professor',
        'form': form,
    })


def signup_student(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('robotic:index')
    if request.method == "POST":
        form = RoboticRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            fullname = form.cleaned_data['fullname']
            cpf = form.cleaned_data['cpf']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                messages.error(request, "Já existe um Usuário ou Email cadastrados, tente com dados diferentes.")
                return redirect('robotic:signup_student', )
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_robotic = RoboticUser.objects.create(user=user, cpf=cpf, fullname=fullname, is_active=False, role="student")
                user.save()
                user_robotic.save()
                return redirect('robotic:index', )
    else:
        form = RoboticRegisterForm()
    return render(request, 'robotic/pages/signup_student.html', {
        'page_name': 'Aluno',
        'form': form,
    })


def signup_teacher(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado!')
        return redirect('robotic:index')
    if request.method == "POST":
        form = RoboticRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            fullname = form.cleaned_data['fullname']
            cpf = form.cleaned_data['cpf']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                messages.error(request, "Já existe um Usuário ou Email cadastrados, tente com dados diferentes.")
                return redirect('robotic:signup_teacher', )
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user_robotic = RoboticUser.objects.create(user=user, cpf=cpf, fullname=fullname, is_active=False, role="teacher")
                user.save()
                user_robotic.save()

                return redirect('robotic:index', )
    else:
        form = RoboticRegisterForm()
        return render(request, 'robotic/pages/signup_teacher.html', {
            'page_name': 'Professor',
            'form': form,
        })


def account_not_active(request):
    user = request.user
    if user.is_authenticated:
        messages.error(request, 'Sua conta ainda não foi ativada por um administrador!')
        return redirect('robotic:index')

    return render(request, 'robotic/pages/account_not_active.html')


def logout_account(request):
    logout(request)
    return redirect('robotic:index')


@login_required(login_url='robotic:login_student')
def root_page(request):
    user = request.user
    robotic_user = RoboticUser.objects.get(user=user)

    if not robotic_user.is_active:
        return redirect('robotic:logout_account')
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
        return redirect('robotic:logout_account')
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
