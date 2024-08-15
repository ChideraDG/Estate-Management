# Generated by Django 5.0.3 on 2024-08-13 09:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("documents", "0001_initial"),
        ("leaseAgreements", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="related_lease",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="documents",
                to="leaseAgreements.leaseagreement",
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="shared_with",
            field=models.ManyToManyField(
                blank=True, related_name="shared_documents", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="uploaded_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="uploaded_documents",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="documentsharing",
            name="document",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sharings",
                to="documents.document",
            ),
        ),
        migrations.AddField(
            model_name="documentsharing",
            name="shared_with",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="received_documents",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
