from django.contrib.auth.models import AbstractUser, User
from django.db import models


class PreviousSite(models.Model):
    image = models.ImageField(upload_to='previous_sites_images/')
    description = models.TextField()
    developer_info = models.CharField(max_length=100)
    site_link = models.URLField()

    def __str__(self):
        return f"Site Anterior - {self.id}"


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class RoboticUser(models.Model):
    CHOICES = [
        ("teacher", 'Teacher'),
        ("staff", 'Staff'),
        ("student", 'Student'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fullname = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    mini_bio = models.TextField(blank=True)
    role = models.CharField(max_length=10, choices=CHOICES, default="student")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    has_certificate = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'RoboticUser - {self.user.username}'
