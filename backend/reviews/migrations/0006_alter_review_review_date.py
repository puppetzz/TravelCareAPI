# Generated by Django 4.0.8 on 2022-12-06 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_review_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 6, 22, 28, 22, 985288)),
        ),
    ]
