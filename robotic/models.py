from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
    full_name = models.CharField(max_length=255)
    mini_bio = models.TextField(blank=True)
    cpf = models.CharField(max_length=11)
    registration = models.CharField(max_length=11)
    foto_perfil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    data_nasc = models.DateField(null=True)
    level_access = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=STUDENT)
    sex = models.CharField(max_length=1)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

class Certificate(models.Model):
    user = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    certificate_date = models.DateField(auto_now_add=True, null=True)
    year = models.CharField(max_length=4)

class Phone(models.Model):
    number = models.CharField(max_length=15)
    whatsapp = models.BooleanField()
    user_phone = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)
