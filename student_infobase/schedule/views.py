from django.shortcuts import render, redirect
from .models import Student, Schedule
from .forms import StudentForm, ScheduleForm

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

def home(request):
    return render(request, 'schedule/home.html')
def login(request):
    return render(request, 'schedule/login.html')