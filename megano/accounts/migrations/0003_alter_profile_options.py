# Generated by Django 4.2.1 on 2023-05-07 12:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_profile_avatar"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={"verbose_name": "profile", "verbose_name_plural": "profiles"},
        ),
    ]
