from collections import OrderedDict
import uuid
from rest_framework import serializers
from .models import Account
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from users.serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    password = serializers.CharField(max_length=68, write_only=True)
    user = UserRegisterSerializer(required=False)

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'email',
            'password',
            'user',
        ]
        
        extra_fields = ['redirect_link']

    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                'The username should only contain alphanumeric character')
        return attrs

    def create(self, validated_data):
        id = str(uuid.uuid4().int)[:9]

        user = validated_data.pop('user')

        account = Account.objects.create_user(id=id, **validated_data)
        user['id'] = id
        user_serializer = UserRegisterSerializer(data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return account


class FormRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68)
    first_name = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    province = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    district = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    street_address = serializers.CharField(max_length=555, required=False, allow_blank=True, allow_null=True)
    redirect_link = serializers.CharField(max_length=255)

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
    redirect_link = serializers.CharField(max_length=255, min_length=1)

    class Meta:
        fields = ['email']
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = [
            'password',
            'confirm_password',
            'token',
            'uidb64',
        ]

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            
            if password != confirm_password:
                raise AuthenticationFailed('password and confirm_password not match.')

            id = force_str(urlsafe_base64_decode(uidb64))
            account = Account.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(account, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            
            account.set_password(password)
            account.save()
            return account
        except Exception:
            raise AuthenticationFailed('The reset link is invalid', 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')