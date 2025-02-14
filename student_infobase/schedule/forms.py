from django import forms
from .models import Schedule, Group, CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['id', 'date', 'time', 'subject']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите ваш login'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Группа", widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'group', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email


    