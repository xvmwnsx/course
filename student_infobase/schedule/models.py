from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.group

class Teacher(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Classes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.name} - {self.group.name} - {self.teacher.name}"

class Schedule(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    subject = models.ForeignKey(Classes, on_delete=models.CASCADE)
    cabinet = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.date} - {self.time} - {self.cabinet}"


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"