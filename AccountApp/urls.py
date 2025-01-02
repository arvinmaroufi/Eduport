from . import views
from django.urls import path

app_name = 'AccountApp'
urlpatterns = [
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    path('sign-in', views.SignInView.as_view(), name='sign-in'),
    path('forget-password', views.ForgetPasswordView.as_view(), name='forget-password'),
    path('verify-code', views.VerifyCodeView.as_view(), name='verify-code'),
    path('reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
]
