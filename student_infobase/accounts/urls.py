from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .autocomplete import TagAutocomplete
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('office/', views.office, name='office'),
    path('vitrina/', views.vitrina, name='vitrina'),
    path('vitrina/add/', views.vitrina_add, name='vitrina_add'),
    path('my_vitrina/', views.my_vitrina, name='my_vitrina'),
    path('vitrina/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('vitrina/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('vitrina/project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),
    path('pending/', views.pending, name='pending'),
    
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
