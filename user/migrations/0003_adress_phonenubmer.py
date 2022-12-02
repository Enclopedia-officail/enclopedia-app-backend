# Generated by Django 3.2 on 2022-03-04 03:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_delete_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='adress',
            name='phoneNubmer',
            field=models.CharField(default=None, max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8, 16}$')]),
        ),
    ]
