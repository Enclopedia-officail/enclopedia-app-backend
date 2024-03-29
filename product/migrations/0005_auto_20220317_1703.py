# Generated by Django 3.2 on 2022-03-17 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_remove_category_slug'),
        ('product', '0004_auto_20220317_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='category.brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='category.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_tag', to='product.Tag'),
        ),
    ]
