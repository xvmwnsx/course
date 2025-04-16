from django.db import models
from accounts.models import CustomUser
from schedule.models import Classes

class Grade(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grades_as_student", verbose_name="Студент")
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grades_as_teacher", verbose_name="Преподаватель")
    grade = models.PositiveSmallIntegerField(verbose_name="Оценка")
    date = models.DateField(verbose_name="Дата")
    is_exam = models.BooleanField(default=False, verbose_name="Экзамен")

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"
    
class PassFailRecord(models.Model):
    PASS_FAIL_CHOICES = [
        ('pass', 'Зачёт'),
        ('fail', 'Незачёт'),
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="pass_fail_records", verbose_name="Студент")
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name="Предмет")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="pass_fail_as_teacher", verbose_name="Преподаватель")
    status = models.CharField(max_length=5, choices=PASS_FAIL_CHOICES, verbose_name="Оценка")
    date = models.DateField(verbose_name="Дата")

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.status}"