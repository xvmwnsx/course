from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('list/', login_required(views.schedule_list), name='schedule_list'),
    path('edit/<int:pk>/', views.schedule_edit, name='schedule_edit'),
    path('search/', login_required(views.schedule_search), name='schedule_search'),
    path('download/', views.download_schedule, name='download_schedule'),
]
