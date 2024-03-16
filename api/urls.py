from django.urls import path, re_path
from . import views

app_name = 'api'

urlpatterns = [
    re_path(r'^users/$', views.users, name="users"),
    re_path(r'^user/register/$', views.user_register, name="user_register"),
    re_path(r'^users/([0-9]+)$', views.users, name="users"),
]