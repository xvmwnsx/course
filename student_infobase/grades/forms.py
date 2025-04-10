from django import forms
from .models import CustomUser, Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'teacher', 'grade', 'date']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['teacher'].queryset = CustomUser.objects.filter(role='teacher')