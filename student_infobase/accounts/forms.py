from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from .models import Vitrina

class StudentProjectForm(forms.ModelForm):
    class Meta:
        model = Vitrina
        fields = ['title', 'description', 'image', 'cover']
        labels = {
            'title': 'Название проекта',
            'description': 'Описание',
            'image': 'Фото (дополнительное)',
            'cover': 'Обложка проекта',
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Старый пароль'}),
        label="Старый пароль"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}),
        label="Новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите новый пароль'}),
        label="Подтверждение пароля"
    )    
    
