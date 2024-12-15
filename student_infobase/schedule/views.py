from django.shortcuts import render, redirect
from .models import Schedule
from .forms import ScheduleForm, LoginForm, UserRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from urllib.parse import quote


class UserLoginView(LoginView):
    template_name = 'schedule/login.html'
    form_class = LoginForm

def home(request):
    return render(request, 'schedule/home.html')

@login_required
def schedule_list(request):
    user = request.user 
    if hasattr(user, 'group') and user.group:
        schedules = Schedule.objects.filter(subject__group=user.group)
    else:
        schedules = []
    return render(request, 'schedule/schedule_list.html', {'schedules': schedules})


def add_schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')
    else:
        form = ScheduleForm()
    return render(request, 'schedule/add_schedule.html', {'form': form})

@login_required
def schedule_search(request):
    query = request.GET.get('q', '')
    results = None
    if query:
        results = Schedule.objects.filter(Q(subject__name__icontains=query) | Q(subject__group__name__icontains=query) ).select_related('subject')  

    return render(request, 'schedule/schedule_search.html', {'query': query, 'results': results})

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
    return render(request, 'schedule/register_user.html', {'form': form})


@login_required  
def office(request):
    user_groups = request.user.groups.all()
    schedule = Schedule.objects.filter(subject__group__name__in=[group.name for group in user_groups])
    return render(request, 'schedule/office.html', {'user': request.user, 'schedule': schedule})

def download_schedule(request):

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Расписание"

    headers = ["ПРЕДМЕТ", "ДАТА", "ВРЕМЯ", "КАБИНЕТ", "ПРЕПОДАВАТЕЛЬ"]
    sheet.append(headers)

    header_font = Font(name='Arial', bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4CAF50", end_color="4CAF50", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    border_style = Side(border_style="thin", color="000000")
    header_border = Border(left=border_style, right=border_style, top=border_style, bottom=border_style)

    for col_num, header in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = header_border

    schedules = Schedule.objects.select_related('subject', 'teacher').all()
    for schedule in schedules:
        teacher_name = f"{schedule.teacher.first_name} {schedule.teacher.last_name}"
        sheet.append([
            schedule.subject.name,
            schedule.date.strftime("%d-%m-%Y"),
            schedule.time.strftime("%H:%M"),
            schedule.cabinet or "—",
            teacher_name,
        ])

    data_alignment = Alignment(horizontal="left", vertical="center")
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, max_col=len(headers)):
        for cell in row:
            cell.alignment = data_alignment
            cell.border = header_border

    for col in sheet.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        sheet.column_dimensions[col_letter].width = max_length + 2

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = "Расписание занятий.xlsx"
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quote(filename)}'
    workbook.save(response)

    return response