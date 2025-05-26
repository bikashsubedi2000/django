from django.shortcuts import render,redirect
from django.http import HttpResponse
from product.models import *
from product.forms import *
from django.contrib import messages
from user.auth import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
@admin_only
def adminhome(request):
    return render(request,'admins/dashboard.html')

@admin_only
def productlist(request):
    product=Product.objects.all()
    return render(request,'admins/productlist.html',{'product':product})

@admin_only
def categorylist(request):
    category=Category.objects.all()
    return render(request,'admins/category.html',{'category':category})

@admin_only
def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'product has been added')
            
            return redirect('/admins/addproduct')  
    else:
        messages.add_message(request,messages.ERROR,'Error occure while adding product')

        form = ProductForm()

    return render(request, 'admins/addproduct.html', {'form': form})
    
@admin_only     
def addcategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES)
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
    
@admin_only 
def updateproduct(request, product_id):
    instance = Product.objects.get(id=product_id)
    if request.method=="POST":
        form=ProductForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'product updated successfully !' )
            return redirect('/admins/productlist')
        else:
            messages.add_message(request, messages.ERROR,'Error occurred While Updating product')
            return render(request,'admins/updateproduct.html',{'form':form})
            
            
    forms = {
        'form': ProductForm(instance=instance)
    }
    return render(request, 'admins/updateproduct.html',forms)

@admin_only
def deleteproduct(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    messages.add_message(request, messages.SUCCESS, 'Product Deleted successfully !')
    return redirect('/admins/productlist')
