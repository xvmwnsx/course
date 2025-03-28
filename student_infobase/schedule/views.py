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
        grades = Grade.objects.all()
        subjects = Classes.objects.all()
        groups = Group.objects.all()

    elif user.role == "teacher":
        subjects = Classes.objects.filter(teacher=user)
        grades = Grade.objects.filter(subject__in=subjects)
        groups = Group.objects.filter(id__in=grades.values_list('student__group_id', flat=True)).distinct()

    else:
        grades = Grade.objects.filter(student=user)
        subjects = Classes.objects.filter(id__in=grades.values_list('subject_id', flat=True))
        groups = None


    subject_id = request.GET.get("subject")
    if subject_id:
        grades = grades.filter(subject_id=subject_id)


    if user.role in ["admin", "teacher"]:
        group_id = request.GET.get("group")
        if group_id:
            grades = grades.filter(student__group_id=group_id)


    can_edit = user.role in ["teacher", "admin"]

    return render(request, 'schedule/grade_list.html', {
        "grades": grades,
        "subjects": subjects,
        "groups": groups,
        "can_edit": can_edit
    })

    
@login_required
def subject_grades(request, subject_id):
    subject = get_object_or_404(Classes, id=subject_id)  
    students = CustomUser.objects.filter(group__classes=subject)
    
    grades = Grade.objects.filter(subject=subject).select_related("student")
    
    grades_by_date = {}
    for grade in grades:
        date_str = grade.date.strftime("%Y-%m-%d")
        if date_str not in grades_by_date:
            grades_by_date[date_str] = {}  
        grades_by_date[date_str][grade.student.id] = grade  

    return render(request, 'schedule/subject_grades.html', {
        'subject': subject,
        'students': students,
        'grades_by_date': grades_by_date
    })

    

@login_required
def grade_edit(request, pk):
    grade_list = get_object_or_404(Grade, pk=pk)
    if request.user.role not in ['teacher', 'admin']:
        return HttpResponseForbidden("У вас нет прав на редактирование оценок.")

    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade_list)
        if form.is_valid():
            form.save()
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade_list)

    return render(request, 'schedule/grade_edit.html', {'form': form})

@login_required
def generate_subject_pdf(request, subject_id):
    subject = Classes.objects.get(id=subject_id)
    grades = Grade.objects.filter(subject=subject)

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter)

    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    p.setFont("DejaVu", 12)

    p.drawString(100, 800, f"Журнал оценок: {subject.name}")

    y_position = 780
    line_height = 14  
    max_line_length = 70  

    def draw_wrapped_text(text, x, y, max_width):
        """
        Функция для автоматического переноса текста.
        """
        lines = []
        current_line = []
        for word in text.split():
            current_line.append(word)
            if p.stringWidth(' '.join(current_line), "DejaVu", 12) > max_width:
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        lines.append(' '.join(current_line)) 

        for line in lines:
            p.drawString(x, y, line)
            y -= line_height
        return y

    for grade in grades:
        text = f"{grade.student.first_name} {grade.student.last_name}: {grade.get_grade_display()} ({grade.date})"
        y_position = draw_wrapped_text(text, 100, y_position, 400)

    p.showPage()
    p.save()

    buffer.seek(0)

    response = FileResponse(buffer, as_attachment=True, filename=f"{subject.name}_grades.pdf")
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
    
def download_schedule(request):
    user = request.user
    user_group = request.user.group 
    schedule = Schedule.objects.filter(subject__group=user_group)
    
    
    if not schedule:
        return HttpResponse("Нет данных для выгрузки", status=404)

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

    for schedule_item in schedule:
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


