from django import forms
from .models import Student, Schedule

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id', 'name', 'group', 'email']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['id', 'date', 'time', 'subject']
