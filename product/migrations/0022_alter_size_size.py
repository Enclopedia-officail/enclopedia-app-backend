# Generated by Django 4.1.2 on 2023-02-21 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_alter_imagegallary_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='size',
            name='size',
            field=models.CharField(choices=[('XXS', 'xxs'), ('XS', 'xs'), ('S', 's'), ('M', 'm'), ('L', 'l'), ('XL', 'xl'), ('XXL', 'xxl'), ('FREE', 'free'), ('26', '26'), ('28', '28'), ('30', '30'), ('32', '32'), ('34', '34'), ('36', '36'), ('38', '38'), ('40', '40'), ('42', '42')], max_length=10),
        ),
    ]