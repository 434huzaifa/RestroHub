# Generated by Django 5.1 on 2024-08-27 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menuSystem", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="menu",
            name="name",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
