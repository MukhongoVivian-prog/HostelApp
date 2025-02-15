# Generated by Django 5.1.3 on 2024-12-05 08:27

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("HostelApp", "0003_booking"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="name",
            field=models.CharField(default=1, max_length=100),
        ),
        migrations.CreateModel(
            name="Hostel",
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
                ("name", models.CharField(max_length=100)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="hostels/"),
                ),
                ("proximity_to_campus", models.CharField(max_length=255)),
                ("amenities", models.TextField()),
                ("address", models.CharField(max_length=255)),
                (
                    "landlord",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hostels",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="room",
            name="hostel",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="HostelApp.hostel",
            ),
        ),
        migrations.CreateModel(
            name="Payment",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Completed", "Completed"),
                            ("Pending", "Pending"),
                            ("Failed", "Failed"),
                        ],
                        default="Pending",
                        max_length=10,
                    ),
                ),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="HostelApp.booking",
                    ),
                ),
            ],
        ),
    ]
