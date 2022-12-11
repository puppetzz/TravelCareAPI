from tokenize import TokenError
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from .serializers import (
    RegisterSerializer,
    FormRegisterSerializer,
    LoginSerializer,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
    LogoutSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.viewsets import ModelViewSet
from .utils import Util
from .models import Account
from .services import Service
from django.shortcuts import get_object_or_404
from users.models import User
from address.models import Address
from django.forms import model_to_dict


class RegisterView(APIView):
    @swagger_auto_schema(request_body=FormRegisterSerializer)
    def post(self, request):
        data = request.data

        user = Service.convert_to_register_data(data)
        serializer = RegisterSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        account = Account.objects.get(id=user_data['id'])
        token = RefreshToken.for_user(account).access_token

        # current_site = get_current_site(request).domain
        # relativeLink = reverse('email-verify', kwargs={'token': token})
        current_site = data['redirect_link']
        absurl = f'http://{current_site}/{token}'
        username = user_data['username']
        email_body = f'Hi {username} Use link below to verify your email. \n{absurl}'
        data = {
            'email_body': email_body,
            'to_email': account.email,
            'domain': absurl,
            'email_subject': 'Verify your email'
        }
        Util.send_email(data)

        return Response(
            {
                "success": 'Successful registration please check your email.'
            }, 
            status=status.HTTP_201_CREATED
        )


class VerifyEmail(APIView):
    def get(self, request, token):
        tokens = token
        try:
            payload = jwt.decode(
                tokens,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            account = Account.objects.get(id=payload['user_id'])
            if not Account.is_verified:
                Account.is_verified = True
                Account.save()

            return Response(
                {
                    'email': 'Successfully activated'
                },
                status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {
                    'error': 'Activation Expired'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {
                    'error': 'Invalid token'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.data

        response = Response({
            'id': account['id'],
            'username': account['username'],
            'email': account['email'],
            'access_token': account['tokens']['access'],
            'refresh_token': account['tokens']['refresh']
        })

        response.set_cookie(
            key='refresh_token',
            value=account['tokens']['refresh'],
            httponly=True
        )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise jwt.InvalidTokenError(e.args[0])

        data = serializer.validated_data

        if 'refresh' in str(data):
            response = Response({
                'access': data['access']
            },
                status=status.HTTP_200_OK)
            response.set_cookie(
                key='refreshtoken',
                value=data['refresh'],
                httponly=True
            )
            return response

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RequestPasswordResetEmailView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordEmailRequestSerializer)
    def post(self, request):
        serializer = ResetPasswordEmailRequestSerializer(data=request.data)

        email = request.data['email']

        if Account.objects.filter(email=email).exists():
            account = Account.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(account.id))
            token = PasswordResetTokenGenerator().make_token(account)
            # current_site = get_current_site(request=request).domain
            # relativeLink = reverse(
            #     'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            current_site = request.data['redirect_link']
            absurl = f'http://{current_site}/{uidb64}/{token}'
            email_body = f'Hello,\nUse link below to reset your password. \n{absurl}'
            data = {
                'email_body': email_body,
                'to_email': account.email,
                'domain': absurl,
                'email_subject': 'Reset your password'
            }
            Util.send_email(data)
            return Response(
                {
                    'success': 'We have sent you a link to reset your password'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'error': 'email does not exits.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class PasswordTokenCheckView(APIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            account = Account.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(account, token):
                return Response(
                    {
                        'error': 'Token is not valid, please request a new one.'
                    },
                    status=status.HTTP_200_OK
                )
            
            return Response(
                {
                    'success': True,
                    'message': 'credentials valid',
                    'uidb64': uidb64,
                    'token': token
                },
                status=status.HTTP_200_OK
            )
        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(account, token):
                return Response(
                    {
                        'error': 'Token is not valid, please request a new one'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

class SetNewPasswordView(APIView):
    @swagger_auto_schema(request_body=SetNewPasswordSerializer)
    def patch(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            {
                'success': True,
                'message': 'Password reset success',
            },
            status=status.HTTP_200_OK
        )
    
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'success': 'Logout success.'
            },
            status=status.HTTP_200_OK
        )

class AccountDeleteView(generics.GenericAPIView):
    
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        account = get_object_or_404(Account, id=id)
        user_data = None
        if User.objects.filter(account=account).exists():
            user = User.objects.get(account=account)
            user_data = model_to_dict(user)
            user.delete()
        if user_data:
            if user_data.get('address'):
                address = get_object_or_404(Address, id=user_data.get('address'))
                address.delete()
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)