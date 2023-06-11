from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.validators import ValidationError

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from .cart import Basket
from .serializers import OrderSerializer
from .models import Order, OrderProducts
from .validators import payment_validator

from products.models import Product


class BasketAPIView(APIView):
    def get(self, request):
        basket = Basket(request)
        return Response(data=basket.get())

    def post(self, request):
        basket = Basket(request)
        basket.add()
        return Response(data=basket.get())

    def delete(self, request):
        basket = Basket(request)
        basket.remove()
        return Response(data=basket.get())


class OrderAPIView(ListModelMixin, LoginRequiredMixin, GenericAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = (
            Order.objects.filter(user=self.request.user)
            .prefetch_related("products")
            .select_related("user")
        )
        return queryset

    def get(self, request):
        return self.list(request)

    def post(self, request):
        data = request.data
        order = Order.objects.create(user=request.user)
        total_cost = 0
        for product_data in data:
            product = Product.objects.get(pk=product_data.get("id"))
            count = min(product.count, int(product_data.get("count")))
            query = OrderProducts.objects.create(
                count=count,
                order=order,
                product=product
            )
            product.count -= count
            total_cost += product.current_price() * count
            query.save()
            product.save()
        order.status = "created"
        order.totalCost = total_cost
        order.save()
        basket = Basket(request)
        basket.clear()
        return Response(data={"orderId": order.id})


class OrderDetailAPIView(UserPassesTestMixin, LoginRequiredMixin, GenericAPIView):
    serializer_class = OrderSerializer

    def test_func(self):
        pk = self.kwargs.get("pk")
        order = Order.objects.get(pk=pk)
        return order.user == self.request.user or self.request.user.is_staff

    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        serialized = OrderSerializer(order)
        return Response(data=serialized.data)

    def post(self, request, pk):
        data = request.data
        serialized = OrderSerializer(data=data)
        if serialized.is_valid():
            order = Order.objects.get(pk=data.get("orderId"))
            validated_data = serialized.validated_data
            serialized.update(order, validated_data)
            delivery_type = "ordinary"
            if not order.deliveryType:
                order.deliveryType = delivery_type = "ordinary"
            if order.totalCost < 50:
                order.totalCost += 10
            if delivery_type == "express":
                order.totalCost += 20
            order.status = "not paid"
            order.save()
            return Response(data={"orderId": order.id})
        return Response(status=400)


class PaymentAPIView(LoginRequiredMixin, UserPassesTestMixin, APIView):
    def test_func(self):
        pk = self.kwargs.get("pk")
        order = Order.objects.get(pk=pk)
        return order.user == self.request.user

    def post(self, request, pk):
        try:
            payment_validator(request)
            order = Order.objects.get(pk=pk)
            order.status = 'paid'
            order.save()
            return Response(status=200)
        except ValidationError:
            return Response(status=400)
