from django.urls import path
from products import views


app_name = "products"


urlpatterns = [
    path("catalog/", views.CatalogAPIView.as_view(), name="get_catalog"),
    path("tags/", views.TagsAPIView.as_view(), name="get_tags"),
    path("categories/", views.CategoryAPIView.as_view(), name="get_categories"),
    path(
        "products/limited/",
        views.LimitedProductsAPIView.as_view(),
        name="get_products_popular",
    ),
    path(
        "products/popular/",
        views.ProductsPopularAPIView.as_view(),
        name="get_products_popular"
    ),
    path(
        "banners/",
        views.BannersAPIView.as_view(),
        name="get_banners"
    ),
    path("sales/", views.SalesAPIView.as_view(), name="get_sales"),
    path(
        "product/<int:pk>/",
        views.ProductDetailAPIView.as_view(),
        name="get_product__id_",
    ),
    path(
        "product/<int:pk>/reviews/",
        views.ProductReviewCreateAPIView.as_view(),
        name="post_product__id__review",
    ),
]
