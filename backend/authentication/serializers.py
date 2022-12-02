from collections import OrderedDict
import uuid
from rest_framework import serializers
from .models import Account
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from users.serializers import UserSerializer
from users.models import User
from django.forms import model_to_dict


class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    password = serializers.CharField(max_length=68, write_only=True)
    user = UserSerializer()

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'email',
            'password',
            'user',
        ]

    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should only contain alphanumeric character')
        return attrs

    def create(self, validated_data):
        print('ok')
        id = str(uuid.uuid4().int)[:9]

        user = validated_data.pop('user')

        account = Account.objects.create_user(id=id, **validated_data)
        user['id'] = id

        user_serializer = UserSerializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return account


class FormRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    country = serializers.CharField(max_length=10)
    province = serializers.CharField(max_length=10)
    district = serializers.CharField(max_length=10)
    street_address = serializers.CharField(max_length=555)

    class Meta:
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):
    id = serializers.CharField(max_length=10, read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'email',
            'password',
            'tokens',
        ]

    def get_tokens(self, obj):
        account = Account.objects.get(email=obj['email'])

        return {
            'access': account.tokens()['access'],
            'refresh': account.tokens()['refresh'],
        }

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        email = attrs.get('email', '')

        account = Account.objects.get(email=email)

        if not account:
            raise AuthenticationFailed('email does not exist.')

        if not account.check_password(password):
            raise AuthenticationFailed('Wrong password')

        if not account.is_active:
            raise AuthenticationFailed('The account is not activated yet!')

        if not account.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'id': account.id,
            'username': account.username,
            'email': account.email,
            'token': account.tokens,
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = [
            'password',
            'token',
            'uidb64',
        ]

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            account = Account.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(account, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            
            account.set_password(password)
            account.save()
            return account
        except Exception:
            raise AuthenticationFailed('The reset link is invalid', 401)
