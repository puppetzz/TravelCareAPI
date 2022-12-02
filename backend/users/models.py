from django.db import models
from authentication.models import Account
from address.models import Address


class User(models.Model):
    account = models.OneToOneField(
        Account, primary_key=True, db_index=True, on_delete=models.CASCADE, db_column='user_id')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, db_index=True, unique=True)
    address = models.OneToOneField(
        Address, on_delete=models.DO_NOTHING, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics', null=True, blank=True)
