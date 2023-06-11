# Generated by Django 4.2.1 on 2023-06-10 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0011_saleproduct"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tags",
                to="products.subcategory",
            ),
            preserve_default=False,
        ),
    ]