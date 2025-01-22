from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.db import models

from .forms import GradeForm
from .models import SchoolClass,CustomUser,Grade

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
       
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password!')
   
    return render(request, 'login.html')

@login_required
def index(request):
    school_classes = request.user.assigned_classes.all()
    context = {
        'school_classes': school_classes
    }
    return render(request, 'index.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Successfully logged out!')
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')

def is_teacher_or_admin(user):
    return user.role in ['moderator', 'admin']

@login_required
@user_passes_test(is_teacher_or_admin)
def class_grades(request, class_id):

    print("User's assigned classes:", [c.name for c in request.user.assigned_classes.all()])
    
    school_class = SchoolClass.objects.get(id=class_id)
    students = CustomUser.objects.filter(assigned_classes=school_class, role='user')
    subjects = request.user.assigned_subjects.all()
    
    if request.method == 'POST':
        form = GradeForm(request.POST, user=request.user)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.teacher = request.user
            grade.save()
            return redirect('class_grades', class_id=class_id)
    else:
        form = GradeForm(user=request.user, 
                        initial={'school_class': school_class})

    students_grades = {}
    for student in students:
        grades = Grade.objects.filter(
            student=student,
            school_class=school_class
        ).order_by('subject', 'date')
        students_grades[student.id] = grades

    context = {
        'school_class': school_class,
        'students': students,
        'subjects': subjects,
        'students_grades': students_grades,
        'form': form,
    }
    return render(request, 'grades/class_grades.html', context)


@login_required
def user_grades(request):
    if request.user.role != 'user':
        return redirect('home') 
        
    grades = Grade.objects.filter(student=request.user).order_by('subject', '-date')
    
    grades_by_subject = {}
    for grade in grades:
        if grade.subject not in grades_by_subject:
            grades_by_subject[grade.subject] = []
        grades_by_subject[grade.subject].append(grade)
    
    context = {
        'grades_by_subject': grades_by_subject,
    }
    return render(request, 'grades/user_grades.html', context)


@login_required
def user_grades(request):
    if request.user.role != 'user':
        return redirect('home')

    grades = Grade.objects.filter(student=request.user).order_by('subject', '-date')
    grades_by_subject = {}
    for grade in grades:
        if grade.subject not in grades_by_subject:
            grades_by_subject[grade.subject] = []
        grades_by_subject[grade.subject].append(grade)

    context = {
        'grades_by_subject': grades_by_subject,
    }
    return render(request, 'grades/user_grades.html', context)


from django.http import JsonResponse

@login_required
@user_passes_test(is_teacher_or_admin)
def manage_grade(request, class_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            form = GradeForm(request.POST, user=request.user)
            if form.is_valid():
                grade = form.save(commit=False)
                grade.teacher = request.user
                grade.save()
                return JsonResponse({
                    'status': 'success',
                    'grade_id': grade.id,
                    'grade_value': grade.grade
                })
            return JsonResponse({'status': 'error'}, status=400)
        
        elif request.method == 'DELETE':
            grade_id = request.GET.get('grade_id')
            try:
                grade = Grade.objects.get(id=grade_id, teacher=request.user)
                grade.delete()
                return JsonResponse({'status': 'success'})
            except Grade.DoesNotExist:
                return JsonResponse({'status': 'error'}, status=404)
    
    school_class = SchoolClass.objects.get(id=class_id)
    students = CustomUser.objects.filter(assigned_classes=school_class, role='user')
    subjects = request.user.assigned_subjects.all()
    
    students_grades = {}
    for student in students:
        grades = Grade.objects.filter(
            student=student,
            school_class=school_class
        ).order_by('subject', 'date')
        students_grades[student.id] = grades

    context = {
        'school_class': school_class,
        'students': students,
        'subjects': subjects,
        'students_grades': students_grades,
        'form': GradeForm(user=request.user, initial={'school_class': school_class}),
    }
    return render(request, 'grades/class_grades.html', context)