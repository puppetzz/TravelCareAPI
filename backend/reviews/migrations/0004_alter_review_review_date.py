# Generated by Django 4.0.8 on 2022-12-05 17:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_review_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 6, 0, 0, 5, 12486)),
        ),
    ]
