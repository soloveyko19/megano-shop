from django.contrib import admin
from .models import (
    Tag,
    Product,
    ProductImages,
    Category,
    Subcategory,
    Review,
    Specification,
    SaleProduct
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"


class ImagesInline(admin.TabularInline):
    model = ProductImages


class ReviewsInline(admin.StackedInline):
    model = Review


class SpecificationsInline(admin.TabularInline):
    model = Specification


class SalesInline(admin.TabularInline):
    model = SaleProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "short_description",
        "count",
        "price",
        "free_delivery",
        "date",
        "category",
    )
    list_display_links = "pk", "title"
    inlines = [
        SalesInline,
        ImagesInline,
        SpecificationsInline,
        ReviewsInline,
    ]

    def get_queryset(self, request):
        return Product.objects.all().select_related("category")


class SubcategoriesInline(admin.TabularInline):
    model = Subcategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    inlines = [
        SubcategoriesInline,
    ]
