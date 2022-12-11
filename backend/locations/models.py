from django.db import models
from address.models import Address

class Category(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=555)


class Location(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    name = models.CharField(max_length=555)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_level = models.IntegerField(null=True)
    description = models.TextField(blank=True, null=True)


