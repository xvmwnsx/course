from django.contrib.auth.models import AbstractUser
from django.db import models

class Group(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f"{self.name or self.id}"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, null=True)
    surname = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    def full_name(self):
        return f"{self.surname} {self.first_name} {self.last_name}".strip()

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    year = models.PositiveIntegerField() 
    faculty = models.CharField(max_length=150)
    department = models.CharField(max_length=150) 
    record_book_number = models.CharField(max_length=50)  
    citizenship = models.CharField(max_length=100) 
    birth_date = models.DateField() 
    admission_year = models.PositiveIntegerField()  
    gpa = models.DecimalField(max_digits=4, decimal_places=2)  

    def __str__(self):
        return f"Студент {self.user.get_full_name()}"

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    faculty = models.CharField(max_length=150)
    department = models.CharField(max_length=150)  
    experience_years = models.PositiveIntegerField()
    position = models.CharField(max_length=100)  

    def __str__(self):
        return f"Преподаватель {self.user.get_full_name()}"
