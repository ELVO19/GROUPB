from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')
def add_student(request):
    return render(request, 'add_student.html')
