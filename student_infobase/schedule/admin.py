from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Classes, Schedule, Group, CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля', {'fields': ('role',)}),
        ('Дополнительные поля', {'fields': ('group',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительные поля', {'fields': ('role',)}),
        ('Дополнительные поля', {'fields': ('group',)}),
    )
    list_display = ['username', 'email', 'group', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Group)
admin.site.register(Schedule)
admin.site.register(Classes)