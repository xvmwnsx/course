from django.contrib import admin
from .models import CustomUser, Group, Student, Teacher, Faculty, Department, Direction, Profile
from django.contrib.auth.admin import UserAdmin
from taggit.models import Tag
from taggit.admin import TagAdmin

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Данные студента'
    fk_name = 'user'

class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Данные преподавателя'
    fk_name = 'user'


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
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        if obj.role == 'student':
            return [StudentInline(self.model, self.admin_site)]
        elif obj.role == 'teacher':
            return [TeacherInline(self.model, self.admin_site)]
        return []


class StudentAdmin(admin.ModelAdmin):
    list_display = ('group', 'user__surname', 'user__first_name', 'user__last_name', 'user', 'year')
    search_fields = ('user__surname', 'user__first_name', 'user__last_name', 'record_book_number')
    list_filter = ('group','year')
    ordering = ('group',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = CustomUser.objects.filter(role='student')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'user', 'faculty', 'department', 'position')
    list_filter = ('faculty', 'department')
    search_fields = ('user__surname', 'user__first_name', 'user__last_name', 'user__username')

    def get_full_name(self, obj):
        return f"{obj.user.surname} {obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'ФИО'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = CustomUser.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('number', 'direction', 'profile', 'get_education_level')
    list_filter = ('direction__education_level', 'profile', 'direction')
    search_fields = ('number',)

    def get_education_level(self, obj):
        return obj.direction.get_education_level_display() if obj.direction else "-"
    get_education_level.short_description = "Уровень образования"


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class DirectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name','faculty', 'education_level')
    list_filter = ('code', 'name', 'faculty', 'education_level')
    search_fields = ('code', 'name')
    ordering = ('faculty',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'direction')
    list_filter = ('direction',)
    search_fields = ('name',)
    

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    list_filter = ('faculty',)
    search_fields = ('name',)

from django import forms
from django.contrib import admin
from taggit.models import Tag
from taggit.managers import TaggableManager
from dal import autocomplete

from .models import Vitrina
from .autocomplete import TagAutocomplete

class VitrinaForm(forms.ModelForm):
    class Meta:
        model = Vitrina
        fields = '__all__'
        widgets = {
            'tags': autocomplete.TaggitSelect2(
                url='tag-autocomplete'
            ),
        }

@admin.register(Vitrina)
class VitrinaAdmin(admin.ModelAdmin):
    form = VitrinaForm
    list_display = ('title', 'student_name', 'created_at', 'tag_list')
    search_fields = ('title', 'student__user__first_name', 'student__user__surname')
    list_filter = ('created_at',)
    autocomplete_fields = ['student']

    def student_name(self, obj):
        return obj.student.user.get_full_name()
    student_name.short_description = 'Студент'

    def tag_list(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    tag_list.short_description = 'Теги'




admin.site.unregister(Tag)
admin.site.register(Tag, TagAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department, DepartmentAdmin)