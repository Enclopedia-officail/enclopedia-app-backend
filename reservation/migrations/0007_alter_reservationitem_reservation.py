# Generated by Django 3.2 on 2022-07-26 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_alter_reservationitem_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationitem',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_reservation_itme', to='reservation.reservation'),
        ),
    ]
