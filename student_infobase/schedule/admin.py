from django.contrib import admin
from .models import Schedule, Classes
from accounts.models import CustomUser

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'get_direction', 'get_profile', 'teacher', 'date', 'time')
    list_filter = ('subject__group__direction', 'subject__group__profile', 'date')
    ordering = ['subject__group__direction__name', 'subject__group__profile__name', 'date', 'time']

    def get_direction(self, obj):
        return obj.subject.group.direction.name if obj.subject and obj.subject.group and obj.subject.group.direction else '—'
    get_direction.short_description = 'Направление'

    def get_profile(self, obj):
        return obj.subject.group.profile.name if obj.subject and obj.subject.group and obj.subject.group.profile else '—'
    get_profile.short_description = 'Профиль'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            kwargs['queryset'] = CustomUser.objects.filter(role='teacher')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return request.user.role != 'student'

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['admin', 'teacher']

class ClassesAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'get_direction', 'get_profile', 'teacher')
    list_filter = ('group__direction', 'group__profile')
    ordering = ['group__direction__name', 'group__profile__name', 'name']

    def get_direction(self, obj):
        return obj.group.direction.name if obj.group and obj.group.direction else '—'
    get_direction.short_description = 'Направление'

    def get_profile(self, obj):
        return obj.group.profile.name if obj.group and obj.group.profile else '—'
    get_profile.short_description = 'Профиль'

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
