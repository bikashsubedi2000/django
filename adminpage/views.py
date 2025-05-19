from django.shortcuts import render,redirect
from django.http import HttpResponse
from product.models import *
from product.forms import *
from django.contrib import messages

# Create your views here.
def adminhome(request):
    return render(request,'admins/dashboard.html')

def productlist(request):
    product=Product.objects.all()
    return render(request,'admins/productlist.html',{'product':product})

def categorylist(request):
    category=Category.objects.all()
    return render(request,'admins/category.html',{'category':category})


def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'product has been added')
            
            return redirect('/admins/addproduct')  
    else:
        messages.add_message(request,messages.ERROR,'Error occure while adding product')

        form = ProductForm()

    return render(request, 'admins/addproduct.html', {'form': form})
    
    
def addcategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Category has been added successfully !')
            return redirect('/admins/addcategory')
        else:
            messages.add_message(request, messages.ERROR, 'Error occure while adding category !')
            return render(request, 'admins/addcategory.html', {'form': form})

    forms = {
        "form": CategoryForm
    }
    return render(request, 'admins/addcategory.html', forms)
    
 
