# Generated by Django 4.1.2 on 2022-12-07 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20220808_0217'),
        ('account_history', '0002_delete_researchhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='is_notification',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_product', to='product.product'),
        ),
    ]
