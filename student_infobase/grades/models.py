from django.db import models
from accounts.models import CustomUser
from schedule.models import Classes

class Grade(models.Model):
    GRADE_CHOICES = [
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grades_as_student", verbose_name="Студент")
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grades_as_teacher", verbose_name="Преподаватель")
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, verbose_name="Оценка")
    date = models.DateField(verbose_name="Дата")

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"

    
class Exam(models.Model):
    EXAM_CHOICES = [
        ('pass', 'Зачёт'),
        ('fail', 'Незачёт'),
        ('5', 'Отлично'),
        ('4', 'Хорошо'),
        ('3', 'Удовлетворительно'),
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="exam_records", verbose_name="Студент")
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="exam_as_teacher", verbose_name="Преподаватель")
    status = models.CharField(max_length=5, choices=EXAM_CHOICES, verbose_name="Оценка")
    date = models.DateField(verbose_name="Дата")

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.status}"