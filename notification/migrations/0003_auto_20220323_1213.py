# Generated by Django 3.2 on 2022-03-23 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_alter_read_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
