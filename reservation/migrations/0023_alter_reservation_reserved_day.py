# Generated by Django 4.1.1 on 2023-09-19 07:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0022_alter_reservation_reserved_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reserved_day',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 19, 7, 32, 50, 293827, tzinfo=datetime.timezone.utc)),
        ),
    ]
