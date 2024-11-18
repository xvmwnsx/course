from django import forms
from .models import Student, Teacher, Subject, Schedule

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'student_id', 'email']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'student', 'date', 'time']
