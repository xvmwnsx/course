from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import gettext as _
from .forms import UserRegistrationForm
from schedule.models import Schedule

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

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')  
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})


@login_required  
def office(request):
    user = request.user
    user_groups = request.user.groups.all()
    schedule = Schedule.objects.filter(
        subject__group__name__in=[group.name for group in user_groups]
        )
    can_edit = user.role in ['teacher', 'admin']
    return render(
        request, 
        'office.html', 
        {'user': request.user, 'can_edit': can_edit, 'schedule': schedule}
        )