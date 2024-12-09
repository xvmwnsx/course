from django import forms
from .models import Student, Schedule
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

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
    

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")
        return cleaned_data