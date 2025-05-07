from django.shortcuts import render, redirect, get_object_or_404
from .models import Schedule
from .forms import ScheduleForm
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.translation import gettext as _
from datetime import timedelta
from django.utils.timezone import now
import pandas as pd
from urllib.parse import quote


@login_required(login_url='/') 
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
        schedules = Schedule.objects.filter(teacher=user.teacher, date__range=[start_of_week, end_of_week])
    elif user.role == 'student':
        if hasattr(user, 'student') and user.student.group:
            schedules = Schedule.objects.filter(subject__group=user.student.group, date__range=[start_of_week, end_of_week])
        else:
            schedules = Schedule.objects.none()
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

@login_required(login_url='/') 
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

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from .models import Schedule

@login_required
def schedule_search(request):
    query = request.GET.get('q', '')
    results = None
    if query:
        results = Schedule.objects.filter(
            Q(subject__name__icontains=query) |
            Q(subject__group__number__icontains=query) |
            Q(subject__group__direction__name__icontains=query) |
            Q(subject__group__profile__name__icontains=query) |
            Q(subject__teacher__surname__icontains=query)
        ).select_related(
            'subject', 'subject__teacher', 'teacher',
            'subject__group__direction', 'subject__group__profile'
        )

    return render(request, 'schedule/schedule_search.html', {
        'query': query,
        'results': results
    })


@login_required(login_url='/')
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
        schedules = Schedule.objects.filter(teacher=user.teacher, date__range=[start_of_week, end_of_week])
    elif user.role == 'student' and hasattr(user, 'student') and user.student.group:
        schedules = Schedule.objects.filter(subject__group=user.student.group, date__range=[start_of_week, end_of_week])
    else:
        schedules = Schedule.objects.none()
    days_of_week = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье"}
    data = []
    for s in schedules:
        teacher_name = f"{s.teacher.first_name} {s.teacher.surname} {s.teacher.last_name}"
        weekday = days_of_week.get(s.date.strftime('%A'), "Неизвестно")
        group = str(s.subject.group)
        data.append({
            "ДЕНЬ НЕДЕЛИ": weekday,
            "ПРЕДМЕТ": s.subject.name,
            "ГРУППА": group,
            "ДАТА": s.date.strftime("%d-%m-%Y"),
            "ВРЕМЯ": s.time.strftime("%H:%M"),
            "КАБИНЕТ": s.cabinet or "—",
            "ПРЕПОДАВАТЕЛЬ": teacher_name,
        })
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = "Расписание занятий.xlsx"
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quote(filename)}'

    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Расписание', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Расписание']
        for i, col in enumerate(df.columns):
            col_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, col_width)
    return response

