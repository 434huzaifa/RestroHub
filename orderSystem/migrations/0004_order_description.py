# Generated by Django 5.1 on 2024-08-27 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orderSystem", "0003_order_created_at_order_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="description",
            field=models.TextField(default=None, null=True),
        ),
    ]