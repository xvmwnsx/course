from django.db import models

class Student(models.Model):
    id = models.IntegerField(max_length=10)
    name = models.CharField(max_length=100)
    group_id = models.IntegerField(max_length=10)
    unique_number = models.IntegerField(max_length=10, unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.subject} - {self.date} - {self.time}"

