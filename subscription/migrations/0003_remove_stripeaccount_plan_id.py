# Generated by Django 3.2 on 2022-05-09 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_alter_stripeaccount_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stripeaccount',
            name='plan_id',
        ),
    ]
