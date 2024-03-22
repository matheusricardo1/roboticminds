from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from datetime import date
from django.utils.text import slugify
import os

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


    def save(self, *args, **kwargs):
        if self.profile_picture:
            username = slugify(self.username)
            ext = os.path.splitext(self.profile_picture.name)[1]
            ext = ext.replace('.', '')
            file_ext_name = ext.upper()
            new_filename = f"profile_pictures/{file_ext_name}/{username}_profile_picture.{ext}"
            
            if not self.profile_picture.name.startswith(new_filename):
                self.profile_picture.name = new_filename

        super(RoboticUser, self).save(*args, **kwargs)

class Certificate(models.Model):
    user = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    certificate_date = models.DateField(auto_now_add=True, null=True)
    year = models.CharField(max_length=4)

class Phone(models.Model):
    number = models.CharField(max_length=15)
    whatsapp = models.BooleanField()
    user_phone = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)


