from rest_framework import serializers
from products.models import Product
from django.db.models import Avg

from .models import Order


class BasketSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    freeDelivery = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_price(self, instance: "Product"):
        return instance.current_price()

    def get_rating(self, instance: "Product"):
        reviews = instance.reviews.all()
        if reviews:
            return round(reviews.aggregate(Avg("rate"))["rate__avg"], 1)

    def get_freeDelivery(self, instance: "Product"):
        return instance.free_delivery

    def get_tags(self, instance: "Product"):
        tags = [
            {
                "id": tag.id,
                "name": tag.name,
            }
            for tag in instance.tags.all()
        ]
        return tags

    def get_images(self, instance: "Product"):
        images = []
        for image in instance.images.all():
            images.append(
                {
                    "src": image.image.url,
                    "alt": image.image.name,
                }
            )
        return images

    def get_reviews(self, instance: "Product"):
        return instance.reviews.count()

    def get_count(self, instance: "Product"):
        basket = self.context.get("basket")
        if basket:
            count = basket.get(str(instance.id))
            return count

    class Meta:
        model = Product
        fields = (
            "id",
            "count",
            "category",
            "price",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        )


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, instance: "Order"):
        if isinstance(instance, Order):
            queryset = instance.products.all()
            products = [
                {
                    "id": product.product.id,
                    "category": product.product.category.id,
                    "price": product.product.current_price(),
                    "count": product.count,
                    "date": product.product.date,
                    "title": product.product.title,
                    "description": product.product.description,
                    "freeDelivery": product.product.free_delivery,
                    "images": [
                        {
                            "src": image.image.url,
                            "alt": image.image.name,
                        }
                        for image in product.product.images.all()
                    ],
                    "tags": [
                        {
                            "id": tag.id,
                            "name": tag.name,
                        }
                        for tag in product.product.tags.all()
                    ],
                    "reviews": product.product.reviews.count(),
                    "rating": round(
                        product.product.reviews.all().aggregate(Avg("rate"))[
                            "rate__avg"
                        ], 1,
                    )
                    if product.product.reviews.first()
                    else None,
                }
                for product in queryset
            ]
            return products

    class Meta:
        model = Order
        fields = (
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        )
