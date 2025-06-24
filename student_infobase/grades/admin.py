from django.contrib import admin
from .models import Grade, Exam
from accounts.models import CustomUser, Student

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("get_group", "student",  "subject", "teacher", "grade", "date")
    list_filter = ("subject", "teacher", "date")
    date_hierarchy = 'date'
    search_fields = (
        'student__last_name', 
        'subject__name', 
        'teacher__last_name',
        'teacher__surname',
        'teacher__first_name', 
        'teacher__email',
        'date',
        'get_group'
        
    ) 
    ordering = ('-date',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(role="student")
        elif db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(role="teacher")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_group(self, obj):
        return obj.student.student.group if obj.student.student else "Без группы"
    get_group.short_description = 'Группа'

    def has_change_permission(self, request, obj=None):
        return request.user.role != 'student'

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['admin', 'teacher']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('get_group', 'subject', 'student', 'status', 'date', 'teacher')
    search_fields = (
        'student__last_name', 
        'subject__name', 
        'teacher__last_name',
        'teacher__surname',
        'teacher__first_name', 
        'teacher__email'
    )  
    list_filter = ('status', 'subject', 'teacher')  
    date_hierarchy = 'date'  
    ordering = ('-date',)  
    fields = ('subject', 'student', 'status', 'date', 'teacher')  

    def get_group(self, obj):
        return obj.student.student.group if obj.student.student else "Без группы"
    get_group.short_description = 'Группа'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            kwargs['queryset'] = CustomUser.objects.filter(role='teacher')
        elif db_field.name == 'student':
            try:
                subject_id = int(request.path.split('/')[-3]) 
                subject = Classes.objects.get(id=subject_id)
                group = subject.group
                student_ids = Student.objects.filter(group=group).values_list('user__id', flat=True)
                kwargs['queryset'] = CustomUser.objects.filter(id__in=student_ids, role='student')
            except Exception as e:
                kwargs['queryset'] = CustomUser.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

