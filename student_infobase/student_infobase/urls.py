from django.contrib import admin
from django.urls import path, include
from student_infobase.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('grades/', include('grades.urls')),    
    path('schedule/', include('schedule.urls')),
    
]

