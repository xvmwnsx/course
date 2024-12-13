from django.contrib import admin
from .models import Teacher, Classes, Schedule, Group, Student

admin.site.register(Teacher)
admin.site.register(Classes)
admin.site.register(Schedule)
admin.site.register(Group)
admin.site.register(Student)