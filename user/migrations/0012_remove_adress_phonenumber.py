# Generated by Django 4.1.2 on 2022-11-13 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_adress_phonenumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adress',
            name='phoneNumber',
        ),
    ]
