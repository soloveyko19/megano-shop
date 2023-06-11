from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from .serializers import (
    ProductCatalogSerializer,
    ProductSerializer,
    TagSerializer,
    CategorySerializer,
    ReviewSerializer,
    SaleSerializer
)
from .filters import ProductFilter, TagFilter, ProductsPopularFilter
from .paginators import CatalogPagination
from .models import Product, Tag, Category, Review


class CatalogAPIView(ListModelMixin, GenericAPIView):
    queryset = (
        Product.objects.all()
        .prefetch_related("images")
        .prefetch_related("tags")
        .prefetch_related("reviews")
        .select_related("sale")
    )
    pagination_class = CatalogPagination
    serializer_class = ProductCatalogSerializer

    filter_backends = [ProductFilter]

    def get(self, request):
        return self.list(request)


class TagsAPIView(ListModelMixin, GenericAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [TagFilter]

    def get(self, request):
        return self.list(request)


class CategoryAPIView(ListModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        response = self.list(request)
        return response


class ProductDetailAPIView(RetrieveModelMixin, GenericAPIView):
    queryset = Product.objects.all().prefetch_related("reviews").select_related("sale")
    serializer_class = ProductSerializer

    def get(self, request, pk):
        return self.retrieve(request)


class ProductReviewCreateAPIView(APIView):
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        serialized = ReviewSerializer(data=request.data)
        if product and serialized.is_valid():
            review = Review.objects.create(
                **serialized.data,
                product=product,
            )
            review.save()

            all_reviews = Review.objects.filter(
                product=product,
            )
            serialized_reviews = ReviewSerializer(all_reviews, many=True)
            return Response(status=200, data=serialized_reviews.data)
        return Response(status=400)


class LimitedProductsAPIView(ListModelMixin, GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_limited=True, is_available=True)[:16]

    def get(self, request):
        return self.list(request)


class SalesAPIView(ListModelMixin, GenericAPIView):
    queryset = Product.objects.filter(sale__isnull=False).select_related("sale")
    serializer_class = SaleSerializer
    pagination_class = CatalogPagination

    def get(self, request):
        return self.list(request)


class ProductsPopularAPIView(ListModelMixin, GenericAPIView):
    queryset = Product.objects.all().select_related("sale")
    serializer_class = ProductCatalogSerializer
    filter_backends = [ProductsPopularFilter]

    def get(self, request):
        return self.list(request)


class BannersAPIView(ListModelMixin, GenericAPIView):
    queryset = Product.objects.filter(is_available=True).select_related("sale")
    serializer_class = ProductCatalogSerializer

    def get(self, request):
        return self.list(request)
