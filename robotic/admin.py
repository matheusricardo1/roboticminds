from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RoboticUserCreationForm, RoboticUserChangeForm
from .models import RoboticUser, Certificate, CertificateAssignment, Project, Event, UserProjectAssignment, UserEventAssignment


class RoboticUserAdmin(UserAdmin):
    add_form = RoboticUserCreationForm
    form = RoboticUserChangeForm
    model = RoboticUser
    list_display = ['level_access', 'username', 'full_name', 'registration']
    fieldsets = (
        ('Robotic', {
            'fields': ('username', 'first_name', 'last_name', 'full_name', 'cpf', 'registration', 'email', 'password', 'level_access', 'profile_picture', 'birth_date', 'is_activated_by_admin'),
        }),
        ('Admin', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'full_name', 'cpf', 'email', 'registration')

admin.site.register(RoboticUser, RoboticUserAdmin)
admin.site.register(Certificate)
admin.site.register(CertificateAssignment)
admin.site.register(Project)
admin.site.register(Event)
admin.site.register(UserProjectAssignment)
admin.site.register(UserEventAssignment)
