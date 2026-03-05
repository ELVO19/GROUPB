from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from Dashboard.models import Student, Payment
from django_daraja.mpesa.core import MpesaClient


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
        date = request.POST.get('date')
        image = request.FILES.get('image')

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
        student.save()
        return redirect('dashboard')
    return render(request, 'update_student.html', {'student': student})


def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate all fields are filled
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'sign_up.html')

        # Check if username already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'sign_up.html')

        # Check if email already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'sign_up.html')

        # Create the new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('dashboard')

    return render(request, 'sign_up.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def payment(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')

        if not phone or not amount:
            messages.error(request, 'All fields are required.')
            return render(request, 'payment.html', {'student': student})

        # Convert 07XX to 2547XX
        if phone.startswith('0'):
            phone = '254' + phone[1:]

        try:
            client = MpesaClient()
            response = client.stk_push(
                phone, int(amount), 'eMobilis',
                'Payment for fee',
                'https://example.com/callback/'
            ).json()
            Payment.objects.create(
                user=request.user,
                phone=phone,
                amount=amount,
                checkout_request_id=response.get('CheckoutRequestID', ''),
                status='pending'
            )
            messages.success(request, 'STK Sent! Check your phone')
        except Exception as e:
            print(e)
            messages.error(request, 'Payment Failed')

    return render(request, 'payment.html', {'student': student})