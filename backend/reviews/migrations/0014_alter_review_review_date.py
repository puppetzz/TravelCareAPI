# Generated by Django 4.0.8 on 2022-12-14 20:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_alter_review_review_date_alter_review_trip_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 15, 3, 24, 28, 30699)),
        ),
    ]
