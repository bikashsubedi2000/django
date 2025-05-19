from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category


# Create your views here.
def product(self):
    return HttpResponse("Welcome to product page")


    

def home(request):
    product=Product.objects.all()
    items={
        'products':product
    }
    return render(request,'index.html',items)

def category(request):
    category=Category.objects.all()
    items={
        'category':category
    }
    return render(request,'category.html',items)

def index(request):
    return render(request,'product/index.html')



