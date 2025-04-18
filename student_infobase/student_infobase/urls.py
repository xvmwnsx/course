from django.contrib import admin
from django.urls import path, include
from student_infobase.views import home_view
from django.contrib.auth.decorators import user_passes_test

def is_not_student(user):
    return user.role != 'student'

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('grades/', include('grades.urls')),    
    path('schedule/', include('schedule.urls')),
    
]

