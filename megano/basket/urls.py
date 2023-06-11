from django.urls import path
from basket import views

app_name = "basket"

urlpatterns = [
    path("basket/", views.BasketAPIView.as_view()),
    path("orders/", views.OrderAPIView.as_view()),
    path("order/<int:pk>/", views.OrderDetailAPIView.as_view()),
    path("payment/<int:pk>/", views.PaymentAPIView.as_view()),
]
