# Generated by Django 4.1.2 on 2023-03-22 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservation", "0016_remove_reservation_payment_method_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="delivery_time",
            field=models.CharField(
                choices=[
                    ("指定なし", "指定なし"),
                    ("午前中", "午前中"),
                    ("12時〜14時頃", "12時〜14時頃"),
                    ("14時〜16時頃", "14時〜16時頃"),
                    ("16時〜18時頃", "16時〜18時頃"),
                    ("18時〜20時頃", "18時〜20時頃"),
                    ("19時〜21時頃", "19時〜21時頃"),
                    ("20時〜21時頃", "20時〜21時頃"),
                ],
                default="指定なし",
                max_length=50,
            ),
        ),
    ]
