from django.urls import path
from .views import (
    UserView
)

urlpatterns = [
    path('get-user/<str:id>', UserView.as_view(), name='get-user')
]
