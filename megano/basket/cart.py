import json
from products.models import Product
from .serializers import BasketSerializer


class Basket:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get("basket")
        if not cart:
            self.session["basket"] = dict()
            cart = self.session.get("basket")
        self.cart = cart

    def add(self):
        data = self.request.data
        product_id = str(data.get("id"))
        count = int(data.get("count"))

        if product_id not in self.cart.keys() and count > 0:
            self.cart[product_id] = count
        elif product_id in self.cart.keys() and count > 0:
            self.cart[product_id] += count
        self.save()

    def get(self):
        queryset = Product.objects.filter(id__in=self.cart.keys())
        serialized = BasketSerializer(
            queryset, many=True, context={"basket": self.cart}
        )
        return serialized.data

    def remove(self):
        data = json.loads(self.request.body)
        product_id = str(data.get("id"))
        count = int(data.get("count"))
        if product_id in self.cart.keys():
            if self.cart.get(product_id) - count > 0:
                self.cart[product_id] -= count
            else:
                del self.cart[product_id]
            self.save()

    def clear(self):
        del self.request.session["basket"]
        self.save()

    def save(self):
        self.session.modified = True
