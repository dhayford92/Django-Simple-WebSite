from django.urls import path
from .views import * # -- calling all classes in the view file

urlpatterns = [
    # -- main url for the store
    path('', Home.as_view(), name="home"),
    path('detail/<int:pk>', DetailPage.as_view(), name="detail"),
    path('cart/', Cart.as_view(), name="cart"),
    path('add-to-cart/<int:pk>', addToCart, name="add-to-cart"),
    path('from-cart/<int:pk>', removeFromCart, name="from-cart"),
    path('checkout/', Checkout.as_view(), name="checkout"),
    
    # -- authentication urls
    path('login', Login.as_view(), name="login"),
    path('register', Register.as_view(), name="register"),
    path('logout', loggingOut, name="logout"),
]
