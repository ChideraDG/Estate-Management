# Generated by Django 5.0.3 on 2024-08-13 13:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="company",
            old_name="owner",
            new_name="user",
        ),
    ]
