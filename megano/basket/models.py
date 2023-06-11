from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import MinValueValidator


class OrderProducts(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )
    count = models.IntegerField(validators=[MinValueValidator(1)])
    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="products"
    )


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    fullName = models.CharField(max_length=150, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15, null=True)
    deliveryType = models.CharField(max_length=50, null=True)
    paymentType = models.CharField(max_length=50, null=True)
    totalCost = models.DecimalField(decimal_places=2, max_digits=100, null=True)
    status = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
        return f"Order #{self.id}"
