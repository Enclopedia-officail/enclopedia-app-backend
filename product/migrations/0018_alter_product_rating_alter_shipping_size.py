# Generated by Django 4.1.1 on 2023-01-14 09:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_size_hem_width_size_rise_alter_size_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='size',
            field=models.CharField(blank=True, choices=[('ネコポス', 'ネコポス'), ('宅急便コンパクト', '宅急便コンパクト'), (0, 0), (60, 60), (80, 80), (100, 100), (120, 120), (140, 140), (160, 160)], max_length=100),
        ),
    ]
