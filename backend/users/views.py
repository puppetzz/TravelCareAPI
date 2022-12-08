from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserProfilePictureUpdateSerializer,
    )
from authentication.models import Account
from .models import User
from django.shortcuts import get_object_or_404
from .service import Service
from authentication.permissions import IsOwner

class UserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        account = get_object_or_404(Account, id=id)
        user = get_object_or_404(User, account=account)
        serializer = self.serializer_class(user)
        data = Service.user_to_view(serializer.data)
        return Response(data, status=status.HTTP_200_OK)

class UserCreateView(generics.GenericAPIView):
    serializer_class = UserUpdateSerializer

    def put(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                'success': True,
                'message': 'Update user success.'
            },
            status=status.HTTP_200_OK)

class UserProfilePictureUpdateView(generics.GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserProfilePictureUpdateSerializer

    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        return Response(
            {
                'success': 'update profile picture success.'
            },
            status=status.HTTP_200_OK
        )