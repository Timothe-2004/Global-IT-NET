# Generated by Django 5.1.7 on 2025-06-08 18:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("gin", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="formation",
            options={"ordering": ["-date_debut"]},
        ),
        migrations.AlterModelOptions(
            name="inscriptionformation",
            options={"ordering": ["-id"]},
        ),
    ]
