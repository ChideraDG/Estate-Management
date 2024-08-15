# Generated by Django 5.0.3 on 2024-08-13 09:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("apartments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentSharing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shared_date", models.DateTimeField(auto_now_add=True)),
                ("access_granted", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("file", models.FileField(upload_to="documents/")),
                (
                    "document_type",
                    models.CharField(
                        choices=[
                            ("lease_agreement", "Lease Agreement"),
                            ("property_document", "Property Document"),
                            ("maintenance_record", "Maintenance Record"),
                            ("financial_report", "Financial Report"),
                            ("other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("upload_date", models.DateTimeField(auto_now_add=True)),
                (
                    "related_apartment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="documents",
                        to="apartments.apartment",
                    ),
                ),
            ],
        ),
    ]
