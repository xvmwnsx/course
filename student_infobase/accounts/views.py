from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.translation import gettext as _
from accounts.models import Student
from django.shortcuts import get_object_or_404
from .models import Vitrina
from .forms import StudentProjectForm
from taggit.models import Tag


def user_login(request):
    if request.method == 'POST':
        form = LoginView(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Успешная аутентификация')
                else:
                    return HttpResponse('Аккаунт отключен')
            else:
                return HttpResponse('Неверный логин')
    else:
        form = LoginView()

    return render(request, 'registration/login.html', {'form': form})

@login_required 
def office(request):
    user = request.user
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        student = None

    can_edit = user.role in ['teacher', 'admin']
    
    user = request.user
    gpa = user.get_gpa()

    return render(
        request, 
        'accounts/office.html', 
        {'user': user, 'student': student,
        'gpa': gpa, 'can_edit': can_edit}
    )

@login_required
def my_vitrina(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return HttpResponseForbidden("Только студенты могут просматривать свои проекты.")

    my_projects = Vitrina.objects.filter(student=student, status='approved').order_by('-created_at')
    return render(request, 'accounts/my_vitrina.html', {'projects': my_projects})

def vitrina(request):
    tag_slug = request.GET.get('tag')
    
    if tag_slug:
        projects = Vitrina.objects.filter(status='approved', tags__slug=tag_slug)
    else:
        projects = Vitrina.objects.filter(status='approved')

    all_tags = Tag.objects.all()

    return render(request, 'accounts/vitrina.html', {
        'projects': projects,
        'all_tags': all_tags,
        'tag_slug': tag_slug,
    })

@login_required
def vitrina_add(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return HttpResponseForbidden("Только студенты могут добавлять проекты.")

    if request.method == 'POST':
        form = StudentProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = student
            project.status = 'pending'
            project.save()
            return redirect('pending')  
    else:
        form = StudentProjectForm()
    return render(request, 'accounts/vitrina_add.html', {'form': form})

def pending(request):
    return render(request, 'accounts/pending.html')

@login_required
def edit_project(request, project_id):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return HttpResponseForbidden("Только студенты могут редактировать проекты.")

    project = get_object_or_404(Vitrina, id=project_id, student=student)

    if request.method == 'POST':
        form = StudentProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = student
            project.status = 'pending'
            project.save()
            return redirect('pending') 
    else:
        form = StudentProjectForm(instance=project)
    return render(request, 'accounts/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, project_id):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        return HttpResponseForbidden("Только студенты могут удалять проекты.")

    project = get_object_or_404(Vitrina, id=project_id, student=student)

    if request.method == 'POST':
        project.delete()
        return redirect('my_vitrina')

    return render(request, 'accounts/confirm_delete_project.html', {'project': project})

def project_detail(request, project_id):
    project = get_object_or_404(Vitrina, id=project_id)
    return render(request, 'accounts/project_detail.html', {'project': project})

