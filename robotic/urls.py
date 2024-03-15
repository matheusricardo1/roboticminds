from django.urls import path
from . import views

app_name = 'robotic'

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_page, name="login"),
    path('signup/', views.signup_page, name="signup"),
    path('logout/', views.logout_page, name="logout"),
    path('account/not-active/', views.account_not_active, name="account_not_active"),
    path('root/', views.root_page, name="root_page"),
    path('root/active/<int:id>/', views.activate_user, name="activate_user"),
]
