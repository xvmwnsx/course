from django.shortcuts import render, redirect
from .models import Student, Schedule
from .forms import StudentForm, ScheduleForm, LoginForm, UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .tokens import email_verification_token
from django.db.models import Q


class UserLoginView(LoginView):
    template_name = 'schedule/login.html'
    form_class = LoginForm

def home(request):
    return render(request, 'schedule/home.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'schedule/student_list.html', {'students': students})

def schedule_list(request):
    schedules = Schedule.objects.all()
    return render(request, 'schedule/schedule_list.html', {'schedules': schedules})


def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'schedule/add_student.html', {'form': form})

def add_schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'schedule/add_schedule.html', {'form': form})


def login_page(request):
    return render(request, 'schedule/login.html')
def forgot_pass(request):
    return render(request, 'schedule/forgot_pass.html')


def schedule_search(request):
    query = request.GET.get('q', '')  # Получить параметр из URL (например, ?q=поиск)
    results = None

    if query:
        results = Schedule.objects.filter(
            Q(subject__name__icontains=query) |  # Поиск по названию предмета
            Q(subject__group__name__icontains=query)  # Поиск по названию группы
        ).select_related('subject')  # Оптимизация для связанных объектов

    return render(request, 'schedule/schedule_search.html', {'query': query, 'results': results})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя в БД
            login(request, user)  # Логиним пользователя после регистрации
            return redirect('home')  # Перенаправляем на главную страницу (или другую)
    else:
        form = UserRegistrationForm()
    return render(request, 'schedule/register_user.html', {'form': form})


@login_required  # Требует авторизации пользователя
def office(request):
    user_groups = request.user.groups.all()  # Получаем группы пользователя
    schedule = Schedule.objects.filter(subject__group__name__in=[group.name for group in user_groups])
    return render(request, 'schedule/office.html', {'user': request.user, 'schedule': schedule})



