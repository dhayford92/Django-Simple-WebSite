from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login




# authentication class for login
class Login(View):
    # get page
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    # send data to server and database
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.warning(request, 'Invalid credentials')
            return render(request, 'authentication/login.html')
        else:
            login(request, user)
            if user.is_staff == True:
                return redirect('dashboard')
            else:
                return redirect('home')
    
   
    
    
# authentication class for login
class Register(View):
    # get page
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    # send data to server and database
    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # -- check if new email exists in the database
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already in used')
            return render(request, 'authentication/register.html')
        # -- check if new username exists in the database
        elif User.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already in used')
            return render(request, 'authentication/register.html')
        else:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname) # -- create user account
            user.save() # -- save the user account
            messages.success(request, 'User account created successfuly')
            return redirect('login')
            
    


# Home view class 
class Home(View):
    def get(self, request):
        items = Product.objects.all()
        return render(request, 'store/home.html', {'items': items})
    
 
 
# -- product detail page class view 
class DetailPage(View):
    def get(self, request, pk):
        item = Product.objects.get(pk=pk)
        context = {
            'item': item
        }
        return render(request,'store/detail.html', context)
    
    
# -- cart view page class
class Cart(View):
    def get(self,request):
        if request.user.is_authenticated:
            try:
                cart = Order.objects.get(user=request.user, is_order=False)
                cartitems = CartItem.objects.filter(user=request.user, is_order=False)
                empty_message = None
            except:
                cart = None
                cartitems = None
                empty_message = "Your cart is empty, Please keep shopping."
            context = {
                'items': cart,
                "cart": cartitems,
                'empty_message': empty_message
            }
            return render(request,'store/cart.html', context)
        else:
            return redirect('login') 


# -- checkout view page class
class Checkout(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Order.objects.filter(user=request.user, is_order=False)
            cartitems = CartItem.objects.filter(user=request.user, is_order=False)
            context = {
                'item': cart,
                "cart": cartitems
                }
            return render(request, 'store/checkout.html', context)
        else:
            return redirect('login')
    
    def post(self, request):
        order = Order.objects.get(user=request.user, is_order=False)
        cartitems = CartItem.objects.filter(user=request.user, is_order=False)
        try:
            order.is_order = True
            for cartitem in cartitems:
                cartitem.is_order = True
                cartitem.save()
            order.save()
            messages.success(request, "Item Ordered successfully")
            return redirect("home")
        except:
            messages.warning(request, "Checkout failed")
            return render(request, 'store/checkout.html')
    
    
    
# -- adding and increasing product in cart function    
def addToCart(request, pk):
    if request.user.is_authenticated:
        item = Product.objects.get(pk=pk) # - get the product id
        cartitem, create = CartItem.objects.get_or_create(user=request.user, item=item, is_order=False) # get or create cartitem with the product item
        order = Order.objects.filter(user=request.user, is_order=False) # get all orders of the user
        if order.exists(): # check if there is an order
            cart = order[0] # - get all order items
            if cart.items.filter(item__pk=pk): # -- check if item exists 
                cartitem.quantity += 1 # --- add 1 anytime the function is call
                cartitem.save()
                cart.total += cartitem.total
                messages.info(request, 'Increase in quantity')
            else:
                cart.items.add(cartitem) # -- add cart item to order list
                cart.get_totalprice
                messages.info(request, 'Item Added to cart')
            return redirect('cart')
        else:
            cart = Order.objects.create(user=request.user, is_order=False, created_on=timezone.now())
            cart.items.add(cartitem)
            cart.total += float(cartitem.total)
            messages.info(request, 'Item Added to cart')
            return redirect('cart')
    else:
        return redirect('login')



# -- removing product from cart function  
def removeFromCart(request, pk):
    item = Product.objects.get(pk=pk)
    cartitem = CartItem.objects.filter(user=request.user, item=item)
    cart_qs = Order.objects.filter(user=request.user, is_order=False)
    if cart_qs.exists(): # -- check if order exists
        cart =  cart_qs[0] # -- get all orders
        if cart.items.count() >= 1: # -- check if cartitem is greater or equal to one
            for citem in cartitem:
                if citem.quantity > 1: 
                    citem.quantity -= 1 
                    cart.total -= citem.total
                    citem.save()
                else:
                    for item in cart_qs:
                        item.items.remove(citem)
                    cart.total -= citem.total
                messages.success(request, 'Item removed')
        else:
            cart_qs.delete()
            messages.success(request, 'Item removed')
    return redirect("cart")


# -- logging user account 
def loggingOut(request):
    logout(request)
    return redirect('home')