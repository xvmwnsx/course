from django.contrib import admin
from .models import CustomUser, Group, Student, Teacher
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': ('surname', 'first_name', 'last_name', 'role'),
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'surname', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'surname', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'surname', 'first_name', 'last_name', 'role')
    ordering = ('username',)
    exclude = ('is_staff', 'is_superuser', 'groups', 'user_permissions')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'department', 'record_book_number', 'admission_year', 'gpa')
    search_fields = ('user__first_name', 'user__surname', 'user__last_name', 'record_book_number')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'department', 'experience_years', 'position')
    search_fields = ('user__first_name', 'user__surname', 'user__last_name', 'department')

admin.site.register(Group)
