from django.db import models
from accounts.models import CustomUser, Group

class Classes(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Преподаватель")

    def __str__(self):
        return f"{self.name}"

class Schedule(models.Model):
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE, verbose_name="Предмет")
    cabinet = models.IntegerField(null=True, blank=True, verbose_name="Кабинет")
    teacher = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, verbose_name="Преподаватель")

    def get_weekday(self):
        return self.date.strftime('%A')  

    def __str__(self):
        return f"{self.subject} {self.date} {self.time} {self.cabinet} {self.teacher}"
