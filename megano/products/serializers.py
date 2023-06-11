from rest_framework import serializers
from django.db.models import Avg

from .models import Product, Tag, Category, Review, Specification


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "id", "name"


class ProductCatalogSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    freeDelivery = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_price(self, instance: "Product"):
        return instance.current_price()

    def get_reviews(self, instance: "Product"):
        return instance.reviews.count()

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

    def get_tags(self, instance: "Product"):
        tags = [
            {
                "id": tag.id,
                "name": tag.name,
            }
            for tag in instance.tags.all()
        ]
        return tags

    def get_freeDelivery(self, instance: "Product"):
        return instance.free_delivery

    def get_rating(self, instance: "Product"):
        reviews = instance.reviews.all()
        if reviews:
            return round(reviews.aggregate(Avg("rate"))["rate__avg"], 1)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "category",
            "freeDelivery",
            "count",
            "price",
            "date",
            "images",
            "tags",
            "rating",
            "reviews",
        )


class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    def get_date(self, instance: "Review"):
        if isinstance(instance, Review):
            return instance.date
        else:
            return None

    class Meta:
        model = Review
        fields = (
            "author",
            "email",
            "text",
            "rate",
            "date",
        )


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = "name", "value"


class ProductSerializer(ProductCatalogSerializer):
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)

    price = serializers.SerializerMethodField()

    def get_price(self, instance: "Product"):
        return instance.current_price()

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "freeDelivery",
            "count",
            "price",
            "date",
            "images",
            "tags",
            "reviews",
            "rating",
            "specifications",
        )


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    def get_subcategories(self, instance: "Category"):
        subcategories = [
            {
                "id": subcategory.id,
                "title": subcategory.name,
                "image": {
                    "src": subcategory.image.url,
                    "alt": subcategory.image.name,
                },
            }
            for subcategory in instance.subcategories.all()
        ]
        return subcategories

    def get_title(self, instance: "Category"):
        return instance.name

    def get_image(self, instance: "Category"):
        return {
            "src": instance.image.url,
            "alt": instance.image.name,
        }

    class Meta:
        model = Category
        fields = "id", "title", "image", "subcategories"


class SaleSerializer(serializers.ModelSerializer):
    salePrice = serializers.SerializerMethodField()
    dateFrom = serializers.SerializerMethodField()
    dateTo = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_salePrice(self, instance: Product):
        return instance.sale.new_price

    def get_dateFrom(self, instance: Product):
        return instance.sale.date_from.strftime("%H:%M %d.%m")

    def get_dateTo(self, instance: Product):
        return instance.sale.date_to.strftime("%H:%M %d.%m")

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

    class Meta:
        model = Product
        fields = "id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"
