from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return f"{self.id}"

class CustomUser(AbstractUser):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} "

class Classes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"

class Schedule(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE)
    cabinet = models.IntegerField(null=True, blank=True)
    teacher = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    
    def get_weekday(self):
        return self.date.strftime('%A')  

    def __str__(self):
        return f"{self.subject} {self.date} {self.time} {self.cabinet} {self.teacher}"

class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grades_as_student")
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grades_as_teacher")
    grade = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.grade}"

