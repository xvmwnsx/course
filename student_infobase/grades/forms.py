from django import forms
from .models import CustomUser, Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'teacher', 'grade', 'date']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['teacher'].queryset = CustomUser.objects.filter(role='teacher')
        
from django import forms
from .models import Exam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['status', 'student', 'date', 'teacher']

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)
        if subject:
            group = subject.group
            students = Student.objects.filter(group=group)
            self.fields['student'].queryset = CustomUser.objects.filter(id__in=students.values_list('user_id', flat=True))

