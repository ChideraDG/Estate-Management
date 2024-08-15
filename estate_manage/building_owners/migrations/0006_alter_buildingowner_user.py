# Generated by Django 5.0.3 on 2024-08-13 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("building_owners", "0005_alter_buildingowner_country_and_more"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buildingowner",
            name="user",
            field=models.OneToOneField(
                blank=True,
                default="",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="building_owners",
                to="users.profile",
            ),
        ),
    ]
