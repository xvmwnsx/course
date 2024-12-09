from django.urls import path
from . import views
from schedule.views import CustomLoginView, CustomLogoutView
from django.contrib.auth.decorators import login_required
from .views import register_user

urlpatterns = [
    path('home/', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
    path('login/', views.login, name='login'),
    path('office/', views.office, name='office'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('student-schedule/', login_required(views.schedule_list), name='student_schedule'),
    path('register-user/', register_user, name='register_user'),
]

