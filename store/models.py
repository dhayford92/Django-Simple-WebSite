from django.db import models
from django.contrib.auth.models import User
    


# Product model class
class Product(models.Model):
    image = models.ImageField(upload_to=True, null=True, blank=True)
    title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    description = models.TextField()
    brand = models.CharField(max_length=500, null=True, blank=True)
    
     # get the title of the category
    def __str__(self):
        return str(self.title)
    
    
    
# CartItem model class for order item
class CartItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, null=True, blank=True)
    is_order = models.BooleanField(default=False)
    
    # get the product name and the user's username
    def __str__(self) -> str:
        return self.item.title + " - " + str(self.user.username)
    
    # getting the total price for the item quantity
    def get_subtotal(self):
        self.total = self.item.price * self.quantity
        return self.total
    
    
    
    
# Order model class for final orders
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    is_payed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_order = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    # get the order id and the user's username
    def __str__(self) -> str:
        return str(self.pk) + " - " + str(self.user.username)
    
    # getting the total price for the items
    def get_totalprice(self):
        for item in self.items.all():
            self.total += item.total
        return self.total