from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Classes, Schedule, Group, CustomUser, Grade

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
        if obj and obj.role in ['admin', 'teacher']:  
            return [fs for fs in fieldsets if 'group' not in fs[1]['fields']]
        return fieldsets

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if request.user.role in ['admin', 'teacher']:
            return [field for field in list_display if field != 'group']
        return list_display 

class ScheduleAdmin(admin.ModelAdmin):
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':  
            kwargs['queryset'] = CustomUser.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if request.user.role == 'student':  
            return False 
        return True 

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['admin', 'teacher'] 
    
class ClassesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':  
            kwargs['queryset'] = CustomUser.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if request.user.role == 'student':  
            return False 
        return True 

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['admin', 'teacher'] 
    
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "teacher", "grade", "date") 
    list_filter = ("subject", "teacher", "date") 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(role="student") 
        elif db_field.name == "teacher":
            kwargs["queryset"] = CustomUser.objects.filter(role="teacher")  
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if request.user.role == 'student':  
            return False 
        return True 

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['admin', 'teacher'] 

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Classes, ClassesAdmin)
admin.site.register(Grade, GradeAdmin)