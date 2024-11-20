from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
]
