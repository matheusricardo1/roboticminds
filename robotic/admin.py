from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import RoboticUser


admin.site.register(RoboticUser)