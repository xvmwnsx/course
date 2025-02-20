from django.shortcuts import render, redirect,get_object_or_404
from .models import Schedule
from .forms import ScheduleForm, UserRegistrationForm
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from urllib.parse import quote


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

    return render(request, 'schedule/login.html', {'form': form})

def home(request):
    return render(request, 'schedule/home.html')

@login_required
def schedule_list(request):
    user = request.user

    if user.role == 'admin':
        # Админ видит всё расписание
        schedules = Schedule.objects.all()
    elif user.role == 'teacher':
        # Учитель видит только своё расписание
        schedules = Schedule.objects.filter(teacher=user)
    else:
        # Студент видит расписание своей группы (если у него есть группа)
        user_groups = user.groups.all()
        if user_groups.exists():
            schedules = Schedule.objects.filter(subject__group__name__in=[group.name for group in user_groups])
        else:
            schedules = []

    # Определяем, можно ли редактировать расписание (только учителям и админам)
    can_edit = user.role in ['teacher', 'admin']

    return render(request, 'schedule/schedule_list.html', {'user': user, 'schedules': schedules, 'can_edit': can_edit})



@login_required
def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)

    # Только учителя и админы могут редактировать расписание
    if request.user.role not in ['teacher', 'admin']:
        return HttpResponseForbidden("У вас нет прав на редактирование расписания.")

    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')  # Перенаправление после сохранения
    else:
        form = ScheduleForm(instance=schedule)

    return render(request, 'schedule/schedule_edit.html', {'form': form})

@login_required
def schedule_search(request):
    query = request.GET.get('q', '')
    results = None
    if query:
        results = Schedule.objects.filter(Q(subject__name__icontains=query) | Q(subject__group__name__icontains=query) ).select_related('subject')  

    return render(request, 'schedule/schedule_search.html', 
                  {'query': query, 'results': results})

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
    schedule = Schedule.objects.filter(
        subject__group__name__in=[group.name for group in user_groups]
        )
    return render(
        request, 
        'schedule/office.html', 
        {'user': request.user, 'schedule': schedule}
        )
    
def download_schedule(request):
    user_group = request.user.group  # Используем именно модель Group, а не auth.Group
    schedule = Schedule.objects.filter(subject__group=user_group)
  
    if not schedule:
        return HttpResponse("Нет данных для выгрузки", status=404)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Расписание"
    
    headers = ["ПРЕДМЕТ", 'НОМЕР ГРУППЫ', 'ГРУППА', "ДАТА", "ВРЕМЯ", "КАБИНЕТ", "ПРЕПОДАВАТЕЛЬ"]
    sheet.append(headers)

    # Стиль для заголовков
    header_font = Font(name='Arial', bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="667eea", end_color="5b74e3", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    border_style = Side(border_style="thin", color="000000")
    header_border = Border(left=border_style, right=border_style, top=border_style, bottom=border_style)

    # Применяем стиль к заголовкам
    for col_num, header in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = header_border

    # Заполняем данные
    for schedule in schedule:
        teacher_name = f"{schedule.teacher.first_name} {schedule.teacher.last_name}"
        sheet.append([
            schedule.subject.name,
            schedule.subject.group.id,
            schedule.subject.group.name,
            schedule.date.strftime("%d-%m-%Y"),
            schedule.time.strftime("%H:%M"),
            schedule.cabinet or "—",
            teacher_name,
        ])

    # Применяем стиль к данным (выравнивание, границы)
    data_alignment = Alignment(horizontal="left", vertical="center")
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, max_col=len(headers)):
        for cell in row:
            cell.alignment = data_alignment
            cell.border = header_border

    # Автоматически подгоняем ширину колонок
    for col in sheet.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        sheet.column_dimensions[col_letter].width = max_length + 2

    # Подготовка ответа для скачивания
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = "Расписание занятий.xlsx"
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quote(filename)}'
    workbook.save(response)

    return response

