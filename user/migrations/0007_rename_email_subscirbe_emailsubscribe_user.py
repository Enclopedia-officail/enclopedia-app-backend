# Generated by Django 3.2 on 2022-04-01 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_emailsubscribe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailsubscribe',
            old_name='email_subscirbe',
            new_name='user',
        ),
    ]
