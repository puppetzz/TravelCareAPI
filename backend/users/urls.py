from django.urls import path
from .views import (
    UserView,
    UserUpdateView,
    UserProfilePictureUpdateView
)

urlpatterns = [
    path('get-user/<str:id>', UserView.as_view(), name='get-user'),
    path('update-user/', UserUpdateView.as_view(), name='update-user'),
    path('update-profile-picture/', UserProfilePictureUpdateView.as_view(), name='update-profile-picture'),
]
