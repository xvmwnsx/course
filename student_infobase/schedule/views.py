from django.shortcuts import render, redirect
from .models import Student, Schedule
from .forms import StudentForm, ScheduleForm, LoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm

class CustomLoginView(LoginView):
    template_name = 'schedule/login.html'
    form_class = LoginForm
    
class CustomLogoutView(LogoutView):
    next_page = 'schedule/home.html'  # Страница после выхода

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


def login(request):
    return render(request, 'schedule/login.html')
def office(request):
    return render(request, 'schedule/office.html')
def forgot_pass(request):
    return render(request, 'schedule/forgot_pass.html')


def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Access denied")
        return _wrapped_view
    return decorator

@role_required(['admin', 'teacher'])
def manage_schedule(request):
    # Only admins and teachers can access
    return render(request, 'schedule/add_schedule.html', 'schedule/add_student.html')


@login_required
def register_user(request):
    if not request.user.is_staff:  # Проверка, что пользователь - администратор
        messages.error(request, "You do not have permission to register users.")
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Установить пароль
            user.save()
            messages.success(request, f"User {user.username} was successfully created.")
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'schedule/register_user.html', {'form': form})





