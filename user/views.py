from django.shortcuts import render
from product.models import *
from .filters import *

# Create your views here.
def homepage(request):
    product = Product.objects.all().order_by('-id')[:4]  # Get last 4 products
    data = {
        'product': product
    }
    return render(request, 'user/homepage.html', data)


def productpage(request):
    product = Product.objects.all().order_by('-id')
    product_filter=ProductFilter(request.GET,queryset=product)
    product_final=product_filter.qs
    data = {
        'product': product_final,
        'product_filter':product_filter
        
    }
    return render(request, 'user/productpage.html',data)

def productdetail(request, product_id):
    product = Product.objects.get(id=product_id)

    data = {
        'product': product
    }

    return render(request, 'user/productdetail.html', data)
