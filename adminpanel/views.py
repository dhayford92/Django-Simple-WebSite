from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from store.models import Order as OrderObject
from store.models import Product as ProductObject
from django.views import View
from django.contrib import messages
import pandas as pd


# -- dashboard class view
class Dashboard(View):
    def get(self, request):
        order_pay = OrderObject.objects.filter(is_order=True, is_payed=True).count()
        order_cal = OrderObject.objects.filter(is_order=True, is_cancelled=True).count()
        order_accp = OrderObject.objects.filter(is_order=True, is_accepted=True).count()
        order = OrderObject.objects.filter(is_order=True, is_accepted=False, is_cancelled=False).order_by('-created_on') # -- get all the orders order by date
        context ={
            'order': order,
            'order_cal': order_cal,
            'order_accp': order_accp,
            'pay_total': order_pay
        }
        return render(request, 'admin/home.html', context)


# -- to accept order by order pk
def acceptOrder(request, pk):
    order = OrderObject.objects.get(pk=pk)
    order.is_accepted = True
    order.save()
    messages.success(request, "Order accepted")
    return redirect('dashboard')

# -- to cancele order by order pk
def cancelOrder(request, pk):
    order = OrderObject.objects.get(pk=pk)
    order.is_cancelled = True
    order.save()
    messages.success(request, "Order cancelled")
    return redirect('dashboard')


class Order(View):
    def get(self, request):
        order = OrderObject.objects.filter(is_order=True).order_by('-created_on')
        return render(request, 'admin/order.html', {'orders': order})
    
    
class Product(View):
    def get(self, request):
        items = ProductObject.objects.all()
        return render(request, 'admin/products.html', {'products': items})
    

# adding product to the database from the csv
def addProduct(request):
    reader = pd.read_json("store/utils/convertcsv.json") # read the data from csv file
    try:
        for _, row in reader.iterrows():
            items = ProductObject(
                image=row['image'],
                title=row['product_name'],
                price=row['retail_price'],
                description=row['description'],
                brand=row['brand'],
            )
            items.save()
        messages.success(request, "Product added Successfully")
    except:
        messages.warning(request, "Product adding error")
    return redirect('product')
    
    
    
class Customers(View):
    def get(self, request):
        user = User.objects.all()
        return render(request, 'admin/customer.html', {'users': user})