# Generated by Django 4.1.2 on 2023-02-26 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscription", "0008_alter_payment_payment_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="payment_id",
            field=models.CharField(max_length=200, null=True),
        ),
    ]