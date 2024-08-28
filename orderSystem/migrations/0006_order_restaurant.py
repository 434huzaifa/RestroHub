# Generated by Django 5.1 on 2024-08-28 05:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orderSystem", "0005_alter_order_totalprice"),
        ("restaurantSystem", "0002_alter_restaurant_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="restaurant",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="restaurant",
                to="restaurantSystem.restaurant",
            ),
            preserve_default=False,
        ),
    ]