# Generated by Django 5.0.6 on 2024-07-04 11:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("estate", "0003_alter_registration_address_2"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="registration",
            name="password",
        ),
    ]
