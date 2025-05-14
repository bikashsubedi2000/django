from django.shortcuts import render
from django.http import HttpResponse
from product.models import *


# Create your views here.
def adminhome(request):
    #return HttpResponse("admin page aayo hai , matlab urls le kam gareko cha ")
    return render(request,'admins/dashboard.html')

def productlist(request):
    product=Product.objects.all()
    return render(request,'admins/productlist.html',{'product':product})

def categorylist(request):
    category=Category.objects.all()
    return render(request,'admins/category.html',{'category':category})