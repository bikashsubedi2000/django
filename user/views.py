from django.shortcuts import render
from product.models import *

# Create your views here.
def homepage(request):
    product = Product.objects.all().order_by('-id')[:4]  # Get last 4 products
    data = {
        'product': product
    }
    return render(request, 'user/homepage.html', data)
