# Generated by Django 4.2.1 on 2023-05-15 14:57

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_subcategory_alter_product_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_available",
            field=models.BooleanField(default=False),
        ),
    ]