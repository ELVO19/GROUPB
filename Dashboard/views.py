from django.shortcuts import render, redirect

from Dashboard.models import Student


# Create your views here.
def dashboard(request):
    students = Student.objects.all()
    return render(request, 'dashboard.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        course = request.POST.get('course')
        age = request.POST.get('age')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        Student.objects.create(
            name=name,
            course=course,
            age=age,
            email=email,
            gender=gender)
        return redirect('dashboard')
    return render(request, 'add_student.html')
