# Generated by Django 5.1 on 2024-08-28 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orderSystem", "0004_order_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="totalPrice",
            field=models.FloatField(default=0),
        ),
    ]
