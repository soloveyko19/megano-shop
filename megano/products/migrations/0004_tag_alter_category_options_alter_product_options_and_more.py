# Generated by Django 4.2.1 on 2023-05-12 11:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_category_product_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name": "tag",
                "verbose_name_plural": "tags",
            },
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "category", "verbose_name_plural": "categories"},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "product", "verbose_name_plural": "products"},
        ),
        migrations.AlterModelOptions(
            name="productimages",
            options={"verbose_name": "image", "verbose_name_plural": "images"},
        ),
        migrations.AddField(
            model_name="product",
            name="tags",
            field=models.ManyToManyField(
                null=True, related_name="products", to="products.tag"
            ),
        ),
    ]
