import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken


class AccountManager(BaseUserManager):
    def create_user(self, id, username, email, password=None):
        if id is None:
            raise TypeError('Users must have a id')
        if username is None:
            raise TypeError('User must have a username')

        account = self.model(
            id=id,
            username=username,
            email=self.normalize_email(email)
        )
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self,
                         username,
                         email,
                         password=None):

        id = str(uuid.uuid4().int)[:9]

        if password is None:
            raise TypeError('Password should not be null')

        account = self.create_user(id, username, email)
        account.is_superuser = True
        account.set_password(password)
        account.save()
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=9, primary_key=True,
                          db_index=True, db_column='user_id')
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    role = models.CharField(max_length=255, default='admin')
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['id', 'username', 'email']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
