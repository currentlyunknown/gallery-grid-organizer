# Generated by Django 4.0.2 on 2022-03-09 06:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("gallery", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="image",
            options={"ordering": ["-weight"]},
        ),
    ]
