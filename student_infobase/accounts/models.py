from django.contrib.auth.models import AbstractUser
from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.name or self.id}"

class CustomUser(AbstractUser):
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
