from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer
from authentication.models import Account
from .models import User
from django.shortcuts import get_object_or_404

class UserView(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        account = get_object_or_404(Account, id=id)
        user = get_object_or_404(User, account=account)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)