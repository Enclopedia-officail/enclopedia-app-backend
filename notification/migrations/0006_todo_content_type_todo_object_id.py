# Generated by Django 4.1.2 on 2023-02-14 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('notification', '0005_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='todo',
            name='object_id',
            field=models.UUIDField(null=True),
        ),
    ]
