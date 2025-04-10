from django import forms
from .models import Schedule, CustomUser

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['id', 'date', 'time', 'subject']
    
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'date', 'time', 'cabinet', 'teacher']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['teacher'].queryset = CustomUser.objects.filter(role='teacher')
        
