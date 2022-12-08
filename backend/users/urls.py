from django.urls import path
from .views import (
    UserView,
    UserCreateView,
    UserProfilePictureUpdateView
)

urlpatterns = [
    path('get-user/<str:id>', UserView.as_view(), name='get-user'),
    path('update-user/', UserCreateView.as_view(), name='update-user'),
    path('update-profile-picture/', UserProfilePictureUpdateView.as_view(), name='update-profile-picture'),
]
