# Generated by Django 3.2 on 2022-06-29 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_product_gender'),
        ('category', '0002_remove_category_slug'),
        ('analytics', '0002_featuredbrand'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardAddItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.IntegerField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_add_brand', to='category.brand')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_add_product', to='product.product')),
            ],
        ),
    ]
