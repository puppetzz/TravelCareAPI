# Generated by Django 4.0.8 on 2022-12-14 15:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_alter_review_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 14, 22, 36, 37, 117965)),
        ),
        migrations.AlterField(
            model_name='review',
            name='trip_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reviews.triptype'),
        ),
    ]
