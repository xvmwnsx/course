from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import gettext as _
from .forms import UserRegistrationForm
from accounts.models import Student, Teacher

def user_login(request):
    if request.method == 'POST':
        form = LoginView(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Успешная аутентификация')
                else:
                    return HttpResponse('Аккаунт отключен')
            else:
                return HttpResponse('Неверный логин')
    else:
        form = LoginView()

    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='/')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            role = form.cleaned_data['role']
            user.role = role
            user.save()

            
            if role == 'student':
                Student.objects.create(user=user)
            elif role == 'teacher':
                Teacher.objects.create(user=user)

            messages.success(request, 'Пользователь успешно зарегистрирован!')
            return redirect('register')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register_user.html', {'form': form})


@login_required 
def office(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        student = None

    can_edit = user.role in ['teacher', 'admin']

    return render(
        request, 
        'accounts/office.html', 
        {'user': user, 'student': student, 'can_edit': can_edit}
    )

