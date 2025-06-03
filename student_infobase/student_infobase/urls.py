from django.contrib import admin
from django.urls import path, include
from student_infobase.views import home_view

from django.conf import settings
from django.conf.urls.static import static

def is_not_student(user):
    return user.role != 'student'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('grades/', include('grades.urls')),    
    path('schedule/', include('schedule.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

