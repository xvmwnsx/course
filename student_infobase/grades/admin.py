from django.contrib import admin
from .models import Grade
from accounts.models import CustomUser

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
        return request.user.role != 'student'

    def has_delete_permission(self, request, obj=None):
        return request.user.role in ['admin', 'teacher']

admin.site.register(Grade, GradeAdmin)
