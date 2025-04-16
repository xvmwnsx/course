from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Grade, Classes, CustomUser, PassFailRecord
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from urllib.parse import quote
from django.utils.translation import gettext as _
import pandas as pd
from accounts.models import Group
from django.db.models import Q


@login_required
def grade_list(request):
    user = request.user

    subjects = Classes.objects.none()
    groups = None

    if user.role == "admin":
        subjects = Classes.objects.all()
        groups = Group.objects.all()
    elif user.role == "teacher":
        subjects = Classes.objects.filter(teacher=user)
        groups = Group.objects.filter(id__in=subjects.values_list("group_id", flat=True)).distinct()
    elif user.role == "student":
        if hasattr(user, "student") and user.student.group:
            subjects = Classes.objects.filter(group=user.student.group)

    subject_id = request.GET.get("subject")
    if subject_id:
        subjects = subjects.filter(id=subject_id)

    if user.role in ["admin", "teacher"]:
        group_id = request.GET.get("group")
        if group_id:
            subjects = subjects.filter(group_id=group_id)

    return render(request, 'grades/grade_list.html', {
        "subjects": subjects,
        "groups": groups,
        "is_teacher_or_admin": user.role in ["admin", "teacher"],
    })



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
        students = CustomUser.objects.filter(student__group=subject.group, role='student').order_by('surname', 'first_name')

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

    # Оценки (числовые)
    grades = Grade.objects.filter(
        subject=subject,
        date__range=[first_day, last_day]
    ).select_related("student")

    if is_student:
        grades = grades.filter(student=user)

    grades_by_date = {date: {} for date in date_list}
    for grade in grades:
        weekday_ru = days_ru[grade.date.strftime("%a")]
        date_str = grade.date.strftime("%d-%m-%y") + f" ({weekday_ru})"
        grades_by_date[date_str][grade.student.id] = f"{grade.grade} (экз)" if grade.is_exam else str(grade.grade)

    # Зачёты и незачёты
    pass_fails = PassFailRecord.objects.filter(
        subject=subject,
        date__range=[first_day, last_day]
    )

    if is_student:
        pass_fails = pass_fails.filter(student=user)

    for record in pass_fails:
        weekday_ru = days_ru[record.date.strftime("%a")]
        date_str = record.date.strftime("%d-%m-%y") + f" ({weekday_ru})"
        grades_by_date.setdefault(date_str, {})[record.student.id] = 'Зачёт' if record.status == 'pass' else 'Незачёт'

    months = {
        1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
        9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
    }

    year_range = list(range(today.year - 5, today.year + 1))

    return render(request, 'grades/subject_grades.html', {
        'subject': subject,
        'students': students,
        'grades_by_date': grades_by_date,
        'date_list': date_list,
        'months': months,
        'year_range': year_range,
        'selected_month': selected_month,
        'selected_year': selected_year,
    })


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

    students = CustomUser.objects.filter(student__group=subject.group, role='student').order_by('surname', 'first_name')
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


    return render(request, 'grades/edit_grades.html', {
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
