from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


def upload_product_images_path(instance: "ProductImages", filename: str) -> str:
    return "products/product_{id}/{filename}".format(
        id=instance.product.id,
        filename=filename,
    )


class Product(models.Model):
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    count = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    free_delivery = models.BooleanField(default=False)
    date = models.DateTimeField()
    category = models.ForeignKey("Subcategory", on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField("Tag", related_name="products")
    is_available = models.BooleanField(default=False)
    is_limited = models.BooleanField(default=False)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return self.title

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key == "count" and self.count == 0:
            self.is_available = False

    def current_price(self):
        try:
            price = self.sale.new_price
            return price
        except SaleProduct.DoesNotExist:
            return self.price

    def short_description(self):
        if len(self.description) > 50:
            return self.description[:47] + " ..."
        else:
            return self.description


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=upload_product_images_path)

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey("Subcategory", on_delete=models.CASCADE, related_name="tags")

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name


def upload_category_photo_path(instance: "Category", filename: str) -> str:
    return "categories/categories/{filename}".format(filename=filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_category_photo_path)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


def upload_subcategory_photo_path(instance: "Subcategory", filename: str) -> str:
    return "categories/subcategories/{filename}".format(filename=filename)


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_subcategory_photo_path)
    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField(max_length=1000, blank=True)
    rate = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    email = models.EmailField()
    author = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"


class Specification(models.Model):
    product = models.ForeignKey(
        Product, related_name="specifications", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)


class SaleProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="sale")
    new_price = models.DecimalField(decimal_places=2, max_digits=100)
    date_from = models.DateTimeField(auto_now_add=True)
    date_to = models.DateTimeField()
