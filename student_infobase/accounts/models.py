from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager

class Faculty(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название факультета")
    
    def __str__(self):
        return f"{self.name}"

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название кафедры")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Факультет")
    
    def __str__(self):
        return f"{self.name}"

class Direction(models.Model):
    BACHELOR = 'bachelor'
    SPECIALIST = 'specialist'
    MASTER = 'master'

    EDUCATION_LEVELS = [
        (BACHELOR, 'Бакалавриат'),
        (SPECIALIST, 'Специалитет'),
        (MASTER, 'Магистратура'),
    ]

    code = models.CharField("Код направления", max_length=10)
    name = models.CharField("Название направления", max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='directions')
    education_level = models.CharField("Уровень образования", max_length=20, choices=EDUCATION_LEVELS, default=BACHELOR)

    def __str__(self):
        return f"{self.code} — {self.name} ({self.get_education_level_display()})"

class Profile(models.Model):  
    name = models.CharField(max_length=100, verbose_name="Название профиля")
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name="Направление")
    
    def __str__(self):
        return f"{self.name}"

class Group(models.Model):
    number = models.PositiveIntegerField(null=True, verbose_name="Номер группы")
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True, verbose_name="Направление")
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, verbose_name="Профиль")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Кафедра")
    
    @property
    def education_level(self):
        return self.direction.education_level if self.direction else None

    def __str__(self):
        direction_name = self.direction.name if self.direction else "Без направления"
        profile_name = self.profile.name if self.profile else "Без профиля"
        return f"{direction_name} / {profile_name} — Группа {self.number}"
    
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, null=True, verbose_name="Имя")
    surname = models.CharField(max_length=150, null=True, verbose_name="Фамилия")
    last_name = models.CharField(max_length=150, null=True, verbose_name="Отчество")
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Админ'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True, verbose_name = "Роль")

    def get_gpa(self):
        exams = self.exam_records.filter(status__in=['3', '4', '5'])
        if not exams.exists():
            return None
        numeric_values = [int(exam.status) for exam in exams]
        return round(sum(numeric_values) / len(numeric_values), 2)

    def full_name(self):
        return f"{self.surname} {self.first_name} {self.last_name}"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, verbose_name="Группа")
    year = models.PositiveIntegerField(null=True, verbose_name="Курс")
    record_book_number = models.CharField(max_length=50, verbose_name="Номер зачетной книжки")
    citizenship = models.CharField(max_length=100, verbose_name="Гражданство")
    birth_date = models.DateField(verbose_name="Дата рождения")
    admission_year = models.PositiveIntegerField(verbose_name="Год поступления")
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, verbose_name="Факультет")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Кафедра")
    
    def __str__(self):
        return f"Студент {self.user.get_full_name()}"

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, verbose_name="Факультет")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Кафедра")
    experience_years = models.PositiveIntegerField(verbose_name="Стаж")
    position = models.CharField(max_length=100, verbose_name="Должность")

    def __str__(self):
        return f"Преподаватель {self.user.get_full_name()}"

class Vitrina(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='project_covers/', null=True, blank=True, verbose_name="Обложка проекта")
    tags = TaggableManager()
    
    def __str__(self):
        return f"{self.title} — {self.student.user.get_full_name()}"