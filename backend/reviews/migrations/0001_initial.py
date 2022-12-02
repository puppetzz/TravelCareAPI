# Generated by Django 4.0.8 on 2022-11-29 14:04

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripType',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('localized_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('review_date', models.DateTimeField(default=datetime.datetime(2022, 11, 29, 21, 4, 39, 153803))),
                ('trip_time', models.DateField()),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField(null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.location')),
                ('trip_type', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='reviews.triptype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='ImageStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=None)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.review')),
            ],
        ),
    ]
