from django.urls import path, include
from .views import (
    RegisterView,
    VerifyEmail,
    LoginView,
    CustomTokenRefreshView,
    RequestPasswordResetEmailView,
    PasswordTokenCheckView,
    SetNewPasswordView,
    LogoutView,
    AccountDeleteView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/<token>', VerifyEmail.as_view(), name='email-verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='refresh-token'),
    path('request-reset-password/', RequestPasswordResetEmailView.as_view(),
         name='request-reset-password'),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckView.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/',
         SetNewPasswordView.as_view(), name='password-reset-complete'),
    path('delete-user/<str:id>', AccountDeleteView.as_view(), name='delete-user'),
]
