from django.db import models
from authentication.models import Account
from address.models import Address


class User(models.Model):
    account = models.OneToOneField(
        Account, primary_key=True, db_index=True, on_delete=models.CASCADE, db_column='user_id')
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, db_index=True, null=True, blank=True)
    address = models.OneToOneField(
        Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics', null=True, blank=True)
