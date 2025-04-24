from django import forms
from .models import Schedule
from accounts.models import CustomUser

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'date', 'time', 'cabinet', 'teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['teacher'].queryset = CustomUser.objects.filter(role='teacher')

        self.fields['teacher'].label_from_instance = lambda obj: f"{obj.surname} {obj.first_name} {obj.last_name}"
