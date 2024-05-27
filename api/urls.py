from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

app_name = 'api'

urlpatterns = [
    re_path(r'^users/token/$', TokenObtainPairView.as_view(), name="get_token"),
    re_path(r'^users/token/refresh/$', TokenRefreshView.as_view(), name="refresh_token"),
    re_path(r'^users/token/verify/$', TokenVerifyView.as_view()),

    re_path(r'^users/$', views.UsersAPI.as_view(),  name="users"),
    re_path(r'^users/([0-9]+)/$', views.UsersAPI.as_view(),  name="users"),
    re_path(r'^user/register/$', views.UserAuth.as_view(), name="users_register"),

    re_path(r'^certificate/$', views.CertificateAPI.as_view(), name="certificate"),
    re_path(r'^certificate/([0-9]+)/$', views.CertificateAPI.as_view(),  name="certificate"),
    re_path(r'^certificate/filter/$', views.CertificateFilterAPI.as_view(),  name="certificate_filter"),
    re_path(r'^certificate/validate/$', views.ValidateCertificateAPI.as_view(), name="validate_certificate"),

    re_path(r'^user_certificate/$', views.CertificateAssignmentAPI.as_view(), name="user_certificate"),
    re_path(r'^user_certificate/([0-9]+)/$', views.CertificateAssignmentAPI.as_view(), name="user_certificate"),
    re_path(r'^user_certificate/filter/$', views.CertificateAssignmentFilterAPI.as_view(), name="user_certificate_filter"),

    path('download_certificate/<int:user_id>/', views.download_certificate, name='download_certificate'),
    #re_path(r'^users/$', views.users, name="users"),
    #re_path(r'^users/([0-9]+)/$', views.users, name="users"),
    #re_path(r'^user/register/$', views.user_register, name="user_register"),
]