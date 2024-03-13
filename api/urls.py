from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.index, name="index"),
    path('login/student/', views.login_student, name="login_student"),
    path('login/teacher/', views.login_teacher, name="login_teacher"),
    path('signup/student/', views.signup_student, name="signup_student"),
    path('signup/teacher/', views.signup_teacher, name="signup_teacher"),
    path('account/logout/', views.logout_account, name="logout_account"),
    path('account/not-active/', views.account_not_active, name="account_not_active"),
    path('root/', views.root_page, name="root_page"),
    path('root/active/<int:id>/', views.activate_user, name="activate_user"),
]
