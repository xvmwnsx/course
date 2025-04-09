from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('office/', views.office, name='office'),
    
    path('schedule-list/', login_required(views.schedule_list), name='schedule_list'),
    path('schedule-edit/<int:pk>/', views.schedule_edit, name='schedule_edit'),
    path('schedule-search/', login_required(views.schedule_search), name='schedule_search'),
    path('download-schedule/', views.download_schedule, name='download_schedule'),
    
    path('register/', views.register, name='register'),
    
    path('grade-list/', views.grade_list, name='grade_list'),
    path('grades/<int:subject_id>/edit/', views.edit_grades, name='edit_grades'),
    path('grades/subject/<int:subject_id>/', views.subject_grades, name='subject_grades'),
    path('export_grades_xlsx/<int:subject_id>/', views.export_grades_xlsx, name='export_grades_xlsx'), 
    path('grades/<int:subject_id>/', views.subject_grades, name='subject_grades'),
    
    path('password-change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    path('password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]

