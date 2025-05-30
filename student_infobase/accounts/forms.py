from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from .models import Vitrina
from django.forms.widgets import ClearableFileInput
from taggit.forms import TagWidget
from taggit.models import Tag
from taggit.forms import TagField

class CustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = ('Удалить файл')  
    
class StudentProjectForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'tag-select'})
    )
    class Meta:
        model = Vitrina
        fields = ['title', 'description', 'image', 'cover', 'tags']
        labels = {
            'title': 'Название проекта',
            'description': 'Описание',
            'image': 'Фото (дополнительное)',
            'cover': 'Обложка проекта',
            'tags': 'Теги'
        }
        widgets = {
            'cover': CustomClearableFileInput(attrs={'class': 'custom-file'}),
            'tags': TagWidget(attrs={'class': 'tag-select'}),
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
    
