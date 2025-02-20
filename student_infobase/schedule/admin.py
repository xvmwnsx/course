from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Classes, Schedule, Group, CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Роль', {'fields': ('role',)}),
        ('Группа', {'fields': ('group',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Роль', {'fields': ('role',)}),
        ('Группа', {'fields': ('group',)}),
    )
    list_display = ['username', 'email', 'group', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.role in ['admin', 'teacher']:  # Скрываем поле group
            return [fs for fs in fieldsets if 'group' not in fs[1]['fields']]
        return fieldsets

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if request.user.role in ['admin', 'teacher']:  # Убираем group из списка
            return [field for field in list_display if field != 'group']
        return list_display 

class ScheduleAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':  
            kwargs['queryset'] = CustomUser.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if request.user.role == 'student':  
            return False  # Студенты не могут редактировать расписание
        return True  # Учителя и админы могут изменять

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['admin', 'teacher']  # Только учителя и админы могут удалять
    
class ClassesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':  
            kwargs['queryset'] = CustomUser.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Classes, ClassesAdmin)