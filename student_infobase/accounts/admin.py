from django.contrib import admin
from .models import CustomUser, Group, Student, Teacher, Faculty, Department, Direction, Profile
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Персональная информация', {
            'fields': ('surname', 'first_name', 'last_name', 'role'),
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'surname', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'surname', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'surname', 'first_name', 'last_name', 'role')
    ordering = ('username', 'email')
    exclude = ('is_staff', 'is_superuser', 'groups', 'user_permissions')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user__surname', 'user__first_name', 'user__last_name', 'user', 'group', 'get_gpa')
    search_fields = ('user__surname', 'user__first_name', 'user__last_name', 'record_book_number')
    list_filter = ('group', 'faculty', 'department')

    def get_gpa(self, obj):
        return obj.gpa if obj.gpa is not None else "—"
    get_gpa.short_description = "GPA"

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'user', 'faculty', 'department', 'position')
    list_filter = ('faculty', 'department')
    search_fields = ('user__surname', 'user__first_name', 'user__last_name', 'user__username')

    def get_full_name(self, obj):
        return f"{obj.user.surname} {obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'ФИО'

    

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('number', 'direction', 'profile', 'get_education_level')
    list_filter = ('direction__education_level', 'profile', 'direction')
    search_fields = ('number',)

    def get_education_level(self, obj):
        return obj.direction.get_education_level_display() if obj.direction else "-"
    get_education_level.short_description = "Уровень образования"



@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'faculty', 'education_level')
    list_filter = ('faculty', 'education_level')
    search_fields = ('code', 'name')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction')
    list_filter = ('direction',)
    search_fields = ('name',)
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    list_filter = ('faculty',)
    search_fields = ('name',)
