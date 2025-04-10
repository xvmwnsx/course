from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Group  # Group можно тут оставить, если модель связана с пользователями

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

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group)

