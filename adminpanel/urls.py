from unicodedata import name
from django.urls import path
from .views import *


urlpatterns = [
    path('', Dashboard.as_view(), name="dashboard"),
    path('accept/<int:pk>', acceptOrder, name="accept"),
    path('cancelled/<int:pk>', cancelOrder, name="cancelled"),
    path('order', Order.as_view(), name="order"),
    path('product', Product.as_view(), name="product"),
    path('addproduct', addProduct, name="addproduct"),
    path('customer', Customers.as_view(), name="customer")
]
