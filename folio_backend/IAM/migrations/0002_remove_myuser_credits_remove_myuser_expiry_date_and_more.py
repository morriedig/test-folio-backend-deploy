# Generated by Django 4.0.3 on 2022-04-03 09:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("IAM", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="myuser",
            name="credits",
        ),
        migrations.RemoveField(
            model_name="myuser",
            name="expiry_date",
        ),
        migrations.RemoveField(
            model_name="myuser",
            name="linkedin_token",
        ),
        migrations.AddField(
            model_name="myuser",
            name="account",
            field=models.CharField(default=django.utils.timezone.now, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="myuser",
            name="username",
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="myuser",
            name="id_number",
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
