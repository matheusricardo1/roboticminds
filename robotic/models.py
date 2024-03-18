from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from datetime import date


class School(models.Model):
    name = models.CharField(max_length=255)
    phone_contact = models.CharField(max_length=60, null=True)
    phone_number = models.CharField(max_length=15)

class RoboticUser(AbstractUser):
    TEACHER = 'teacher'
    STAFF = 'staff'
    STUDENT = 'student'
    LEVEL_CHOICES = [
        (TEACHER, 'Teacher'),
        (STAFF, 'Staff'),
        (STUDENT, 'Student'),
    ]
    
    full_name = models.CharField(max_length=255, blank=True)
    mini_bio = models.TextField(blank=True)
    cpf = models.CharField(max_length=11, blank=True, unique=True)
    registration = models.CharField(max_length=11, blank=True, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True) 
    birth_date = models.DateField(default=date(2000, 1, 1), blank=True)
    level_access = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=STUDENT)
    sex = models.CharField(max_length=1, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True) 
    is_activated_by_admin = models.BooleanField(default=False)

class Certificate(models.Model):
    user = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    certificate_date = models.DateField(auto_now_add=True, null=True)
    year = models.CharField(max_length=4)

class Phone(models.Model):
    number = models.CharField(max_length=15)
    whatsapp = models.BooleanField()
    user_phone = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)


