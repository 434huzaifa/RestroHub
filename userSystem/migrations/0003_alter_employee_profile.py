# Generated by Django 5.1 on 2024-08-26 18:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userSystem", "0002_alter_owner_restaurants"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="profile",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="userSystem.profile",
            ),
        ),
    ]
