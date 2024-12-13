from django.urls import path
from . import views
from schedule.views import UserLoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from .views import register

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('schedule_list/', views.schedule_list, name='schedule_list'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
    path('login/', views.LoginView.as_view(template_name='schedule/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('office/', views.office, name='office'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('student-schedule/', login_required(views.schedule_list), name='student_schedule'),
    path('register/', views.register, name='register'),
    path('schedule_search/', views.schedule_search, name='schedule_search'),

]

