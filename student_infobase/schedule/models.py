from django.db import models
from accounts.models import CustomUser, Group

class Classes(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Schedule(models.Model):
    date = models.DateField()
    time = models.TimeField()
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE)
    cabinet = models.IntegerField(null=True, blank=True)
    teacher = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)

    def get_weekday(self):
        return self.date.strftime('%A')  

    def __str__(self):
        return f"{self.subject} {self.date} {self.time} {self.cabinet} {self.teacher}"
