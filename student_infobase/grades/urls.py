from django.urls import path
from . import views

urlpatterns = [
    path('', views.grade_list, name='grade_list'),
    path('<int:subject_id>/edit/', views.edit_grades, name='edit_grades'),
    path('exam/<int:exam_id>/edit', views.edit_exam, name='edit_exam'),
    path('exams/<int:subject_id>/view/', views.view_exam, name='view_exam'),
    path('subject/<int:subject_id>/', views.subject_grades, name='subject_grades'),
    path('export_xlsx/<int:subject_id>/', views.export_grades_xlsx, name='export_grades_xlsx'),
]
