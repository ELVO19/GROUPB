from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User  # Corrected Import
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages  # Corrected Import
from Dashboard.models import Student


def dashboard(request):
    students = Student.objects.all()
    return render(request, 'dashboard.html', {'students': students})
def add_student(request):
    if request.method == 'POST':
        # Correct handling of POST data and FILES
        name = request.POST.get('name')
        course = request.POST.get('course')
        age = request.POST.get('age')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        date = request.POST.get('date')
        image = request.FILES.get('image')  # Correct way to get file

        Student.objects.create(
            image=image,
            name=name,
            course=course,
            age=age,
            email=email,
            gender=gender,
            date=date
        )
        return redirect('dashboard')
    return render(request, 'add_student.html')


def update_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.course = request.POST.get('course')
        student.age = request.POST.get('age')
        student.email = request.POST.get('email')
        student.gender = request.POST.get('gender')
        student.date = request.POST.get('date')

        # Handle file update
        if request.FILES.get('image'):
            student.image = request.FILES['image']

        student.save()
        return redirect('dashboard')
    return render(request, 'update_student.html', {'student': student})
def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'sign_up.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # Basic validation
        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('login')