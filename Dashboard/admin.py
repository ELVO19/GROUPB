from django.contrib import admin

from Dashboard.models import Student, Exam, Payment

# Register your models here.
admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(Payment)