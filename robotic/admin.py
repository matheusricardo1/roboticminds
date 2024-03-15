from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RoboticUserCreationForm, RoboticUserChangeForm
from .models import RoboticUser


class RoboticUserAdmin(UserAdmin):
    add_form = RoboticUserCreationForm
    form = RoboticUserChangeForm
    model = RoboticUser
    list_display = ['level_access', 'username', 'full_name', 'registration']
    fieldsets = (
        ('Robotic', {
            'fields': ('username', 'first_name', 'last_name', 'full_name', 'cpf', 'registration', 'email', 'password', 'level_access', 'foto_perfil', 'data_nasc'),
        }),
        ('Admin', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'full_name', 'cpf', 'email', 'registration')

admin.site.register(RoboticUser, RoboticUserAdmin)
