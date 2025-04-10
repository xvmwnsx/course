from django.db import models
from accounts.models import CustomUser
from schedule.models import Classes

class Grade(models.Model):
    GRADE_CHOICES = [
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('pass', 'Зачёт'),
        ('fail', 'Незачёт'),
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grades_as_student")
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grades_as_teacher")
    grade = models.CharField(max_length=5, choices=GRADE_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"
