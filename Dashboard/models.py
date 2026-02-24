from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=20)
    course = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()
    gender = models.CharField(
        max_length=20,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
        ],
        default='Male',)

    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=20)
    exam_code = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.name