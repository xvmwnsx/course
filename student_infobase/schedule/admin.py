from django.contrib import admin
from .models import Schedule, Classes
from accounts.models import CustomUser

class ScheduleAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':  
            kwargs['queryset'] = CustomUser.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return request.user.role != 'student'

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['admin', 'teacher']

class ClassesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':  
            kwargs['queryset'] = CustomUser.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return request.user.role != 'student'

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['admin', 'teacher']

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Classes, ClassesAdmin)
