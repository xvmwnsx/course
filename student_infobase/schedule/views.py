from django.shortcuts import render, redirect,get_object_or_404
from .models import Schedule, Grade, Group, Classes, CustomUser
from .forms import ScheduleForm, UserRegistrationForm, GradeForm
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
from django.utils.translation import gettext as _
from datetime import timedelta
from django.utils.timezone import now
from django.http import FileResponse
from reportlab.pdfgen import canvas
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter


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
def grade_list(request):
    user = request.user

    if user.role == "admin":
        subjects = Classes.objects.all()
        groups = Group.objects.all()
    elif user.role == "teacher":
        subjects = Classes.objects.filter(teacher=user)
        groups = Group.objects.filter(id__in=subjects.values_list("group_id", flat=True)).distinct()
    else:
        subjects = Classes.objects.filter(group=user.group)
        groups = None

    subject_id = request.GET.get("subject")
    if subject_id:
        subjects = subjects.filter(id=subject_id)

    if user.role in ["admin", "teacher"]:
        group_id = request.GET.get("group")
        if group_id:
            subjects = subjects.filter(group_id=group_id)

    return render(request, 'schedule/grade_list.html', {
        "subjects": subjects,
        "groups": groups,
        "is_teacher_or_admin": user.role in ["admin", "teacher"],
    })

from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from .models import Grade, Classes, CustomUser

days_ru = {
    'Mon': 'Пн', 'Tue': 'Вт', 'Wed': 'Ср', 'Thu': 'Чт', 'Fri': 'Пт', 'Sat': 'Сб', 'Sun': 'Вс'
}

def subject_grades(request, subject_id):
    subject = get_object_or_404(Classes, id=subject_id)  
    user = request.user  

    is_student = user.role == 'student'

    if is_student:
        students = CustomUser.objects.filter(id=user.id)
    else:
        students = CustomUser.objects.filter(group__classes=subject).order_by('last_name', 'first_name')

    today = datetime.today()
    selected_month = int(request.GET.get('month', today.month))
    selected_year = int(request.GET.get('year', today.year))
    
    if selected_month in [7, 8]:
        selected_month = 9 
    
    first_day = datetime(selected_year, selected_month, 1)
    last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    
    date_list = []
    current_day = first_day
    while current_day <= last_day:
        if current_day.weekday() != 6:  
            weekday_ru = days_ru[current_day.strftime("%a")]
            date_list.append(current_day.strftime("%d-%m-%y") + f" ({weekday_ru})") 
        current_day += timedelta(days=1)

    grades = Grade.objects.filter(subject=subject, date__range=[first_day, last_day]).select_related("student")

    if is_student:
        grades = grades.filter(student=user)

    grades_by_date = {date: {} for date in date_list}
    for grade in grades:
        weekday_ru = days_ru[grade.date.strftime("%a")]
        date_str = grade.date.strftime("%d-%m-%y") + f" ({weekday_ru})"
        grades_by_date[date_str][grade.student.id] = grade.grade 

    months = {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
        9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }

    year_range = list(range(today.year - 5, today.year + 1))

    return render(request, 'schedule/subject_grades.html', {
        'subject': subject,
        'students': students,
        'grades_by_date': grades_by_date,
        'date_list': date_list,
        'months': months,
        'year_range': year_range,
        'selected_month': selected_month,
        'selected_year': selected_year,
    })

from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta
from .models import Grade, Classes, CustomUser

def edit_grades(request, subject_id):
    
    days_ru = {
    'Mon': 'Пн', 'Tue': 'Вт', 'Wed': 'Ср', 'Thu': 'Чт', 'Fri': 'Пт', 'Sat': 'Сб', 'Sun': 'Вс'
}
    
    subject = get_object_or_404(Classes, id=subject_id)
    today = datetime.today()

    selected_month = int(request.GET.get('month', today.month))
    selected_year = int(request.GET.get('year', today.year))


    if selected_month in [7, 8]:
        selected_month = 9

    first_day = datetime(selected_year, selected_month, 1)
    last_day = (first_day + timedelta(days=31)).replace(day=1) - timedelta(days=1)


    date_list = []
    current_day = first_day
    while current_day <= last_day:
        if current_day.weekday() != 6:
            weekday_ru = days_ru[current_day.strftime("%a")]
            date_list.append(current_day.strftime("%d-%m-%y") + f" ({weekday_ru})")
        current_day += timedelta(days=1)

    students = CustomUser.objects.filter(group__classes=subject, role='student').order_by('last_name', 'first_name')
    grades = Grade.objects.filter(subject=subject, date__range=[first_day, last_day])


    grade_dict = {}
    for grade in grades:
        key = (grade.student.id, grade.date.strftime("%d-%m-%y") + f" ({days_ru[grade.date.strftime('%a')]})")
        grade_dict[key] = grade.grade

    grade_choices = Grade.GRADE_CHOICES

    months = {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
        9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }
    year_range = list(range(today.year - 5, today.year + 1))
    
    if request.method == 'POST':
        for student in students:
            for date_str in date_list:
                key = f"grade_{student.id}_{date_str}"
                grade_value = request.POST.get(key)
                if grade_value:
                    date = datetime.strptime(date_str[:8], "%d-%m-%y").date()
                    grade, created = Grade.objects.get_or_create(
                        student=student,
                        subject=subject,
                        date=date,
                        defaults={'teacher': request.user, 'grade': grade_value}
                    )
                    if not created:
                        grade.grade = grade_value
                        grade.save()
        return redirect(request.path + f"?month={selected_month}&year={selected_year}")


    return render(request, 'schedule/edit_grades.html', {
        'subject': subject,
        'students': students,
        'date_list': date_list,
        'grade_dict': grade_dict,
        'grade_choices': grade_choices,
        'months': months,
        'year_range': year_range,
        'selected_month': selected_month,
        'selected_year': selected_year,
    })





import pandas as pd
from urllib.parse import quote

def export_grades_xlsx(request, subject_id):
    subject = get_object_or_404(Classes, id=subject_id)  
    grades = Grade.objects.filter(subject=subject).order_by('student__last_name', 'date')  

    data = []
    for grade in grades:
        data.append([
            grade.student.last_name,
            grade.student.first_name,
            grade.date.strftime('%Y-%m-%d'),
            grade.grade
        ])
    
    df = pd.DataFrame(data, columns=['Фамилия', 'Имя', 'Дата', 'Оценка'])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    subject_name = subject.name.replace(" ", "_")  
    filename = f"grades_{subject_name}.xlsx"

    quoted_filename = quote(filename)  
    response['Content-Disposition'] = f'attachment; filename="{filename}"; filename*=UTF-8\'\'{quoted_filename}'

    
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Оценки')
    
    return response



@login_required
def schedule_list(request): 
    user = request.user

    try:
        week_offset = int(request.GET.get("week_offset", 0))
    except ValueError:
        week_offset = 0

    today = now().date()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=5) 

    if user.role == 'admin':
        schedules = Schedule.objects.filter(date__range=[start_of_week, end_of_week])
    elif user.role == 'teacher':
        schedules = Schedule.objects.filter(teacher=user, date__range=[start_of_week, end_of_week])
    elif user.role == 'student' and user.group:
        schedules = Schedule.objects.filter(subject__group=user.group, date__range=[start_of_week, end_of_week])
    else:
        schedules = Schedule.objects.none()
    
    week_days_translation = {
        "Monday": _("Понедельник"),
        "Tuesday": _("Вторник"),
        "Wednesday": _("Среда"),
        "Thursday": _("Четверг"),
        "Friday": _("Пятница"),
        "Saturday": _("Суббота"),
    }
    week_days = list(week_days_translation.values())


    grouped_schedules = {day: [] for day in week_days}
    for schedule in schedules:
        english_day = schedule.date.strftime("%A") 
        russian_day = week_days_translation.get(english_day, None)  
        if russian_day:
            grouped_schedules.setdefault(russian_day, []).append(schedule) 

    can_edit = user.role in ['teacher', 'admin']

    return render(request, 'schedule/schedule_list.html', {
        'schedules': grouped_schedules,
        'can_edit': can_edit,
        'week_days': week_days,
        'week_offset': week_offset,
        'prev_week_offset': week_offset - 1,
        'next_week_offset': week_offset + 1,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week
    })

@login_required
def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.user.role not in ['teacher', 'admin']:
        return HttpResponseForbidden("У вас нет прав на редактирование расписания.")

    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')
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
    
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from django.http import HttpResponse
from urllib.parse import quote
from django.utils.timezone import now
from datetime import timedelta

def download_schedule(request):
    user = request.user

    try:
        week_offset = int(request.GET.get("week_offset", 0))
    except ValueError:
        week_offset = 0

    today = now().date()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=5) 

    if user.role == 'admin':
        schedules = Schedule.objects.filter(date__range=[start_of_week, end_of_week])
    elif user.role == 'teacher':
        schedules = Schedule.objects.filter(teacher=user, date__range=[start_of_week, end_of_week])
    elif user.role == 'student' and user.group:
        schedules = Schedule.objects.filter(subject__group=user.group, date__range=[start_of_week, end_of_week])
    else:
        schedules = Schedule.objects.none()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Расписание"

    headers = ["ДЕНЬ НЕДЕЛИ", "ПРЕДМЕТ", 'НОМЕР ГРУППЫ', 'ГРУППА', "ДАТА", "ВРЕМЯ", "КАБИНЕТ", "ПРЕПОДАВАТЕЛЬ"]
    sheet.append(headers)

    header_font = Font(name='Arial', bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="667eea", end_color="5b74e3", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    border_style = Side(border_style="thin", color="000000")
    header_border = Border(left=border_style, right=border_style, top=border_style, bottom=border_style)

    for col_num, header in enumerate(headers, start=1):
        cell = sheet.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = header_border

    days_of_week = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье"
    }

    for schedule_item in schedules:
        teacher_name = f"{schedule_item.teacher.first_name} {schedule_item.teacher.last_name}"
        weekday = days_of_week.get(schedule_item.date.strftime('%A'), "Неизвестно")

        sheet.append([
            weekday,
            schedule_item.subject.name,
            schedule_item.subject.group.id,
            schedule_item.subject.group.name,
            schedule_item.date.strftime("%d-%m-%Y"),
            schedule_item.time.strftime("%H:%M"),
            schedule_item.cabinet or "—",
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