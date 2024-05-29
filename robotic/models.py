import os
from random import randint
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


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
    birth_date = models.DateField(default=date(2000, 1, 1), blank=True, null=True)
    level_access = models.CharField(max_length=20, choices=LEVEL_CHOICES, default=STUDENT)
    sex = models.CharField(max_length=1, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    is_activated_by_admin = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.is_superuser == True and self.level_access != "teacher":
            self.level_access == "teacher"
        if self.level_access == "teacher":
            self.is_superuser = True
        
        if not self.cpf:
            self.cpf = str(randint(00000000000, 99999999999))
        if not self.registration:
            self.registration = str(randint(00000000000, 99999999999))

        if self.profile_picture:
            username = slugify(self.username)
            ext = os.path.splitext(self.profile_picture.name)[1]
            ext = ext.replace('.', '')
            file_ext_name = ext.upper()
            new_filename = f"{file_ext_name}/{username}_profile_picture.{ext}"
            if not self.profile_picture.name.startswith(new_filename):
                self.profile_picture.name = new_filename
        super(RoboticUser, self).save(*args, **kwargs)


class Certificate(models.Model):
    name = models.CharField(max_length=255)
    details = models.CharField(max_length=120)
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.CharField(max_length=255, default="Manacapuru")
    hours = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f'{self.name}'


class CertificateAssignment(models.Model):
    user = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, unique=True, blank=True)
    assignment_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = f'{randint(10000000, 99999999)}.{randint(1000000, 9999999)}.{randint(100000, 999999)}.{randint(0, 9)}.{randint(1000000000000000000, 9999999999999999999)}'
        super(CertificateAssignment, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.certificate.name} - {self.user.username}'


class Phone(models.Model):
    number = models.CharField(max_length=15)
    whatsapp = models.BooleanField()
    user_phone = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('completed', 'Completed')], default='active')

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class UserProjectAssignment(models.Model):
    user = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    assignment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.project.name} - {self.user.username}'

class UserEventAssignment(models.Model):
    user = models.ForeignKey(RoboticUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    assignment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.event.name} - {self.user.username}'