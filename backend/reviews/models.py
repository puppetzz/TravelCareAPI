from django.db import models
from locations.models import Location
from users.models import User
from datetime import datetime, timedelta


def generate_unique_name(path):
    pass


class TripType(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    localized_name = models.CharField(max_length=255)


class Review(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review_date = models.DateTimeField(
        default=(datetime.utcnow() + timedelta(hours=7)))
    trip_time = models.DateField()
    trip_type = models.ForeignKey(TripType, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True)


class ImageStorage(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.ImageField()
