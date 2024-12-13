from django import forms
from .models import Student, Schedule, Group, CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id', 'name', 'group', 'email']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['id', 'date', 'time', 'subject']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Введите ваш login'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Введите ваш email'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'group', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email


    