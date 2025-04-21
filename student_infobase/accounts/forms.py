from django import forms
from .models import Group, CustomUser
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=150)
    surname = forms.CharField(label="Фамилия", max_length=150)
    last_name = forms.CharField(label="Отчество (при наличии)", max_length=150)
    username = forms.CharField(
        label='Логин'
        )
    email = forms.EmailField(
        label="Email",
        )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), 
        required=True, 
        label="Группа",
        widget=forms.Select(attrs={'class': 'form-control'})
        )

    password1 = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Минимум 8 символов. Не используйте слишком простые пароли."
    )
    password2 = forms.CharField(
        required=True,
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Введите тот же пароль для подтверждения."
    )
    
    class Meta:
        model = CustomUser
        fields = [
                  'first_name', 'surname', 'last_name', 
                  'username', 'email', 
                  'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email


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