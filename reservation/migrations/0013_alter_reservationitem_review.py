# Generated by Django 4.1.1 on 2023-01-16 07:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0012_reservation_return_date_reservationitem_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationitem',
            name='review',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
    ]
