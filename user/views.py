from django.shortcuts import render,redirect
from product.models import *
from .filters import *

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate,login,logout
from .forms import *

from user.auth import *
from django.urls import reverse


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'User account has been created successfully.')
            return redirect('/register')
        else:
            messages.add_message(request, messages.ERROR, 'Please provide correct credentials.')
            return render(request, 'user/register.html', {'form': form})

    context = {
        'form': UserCreationForm()
    }
    return render(request, 'user/register.html', context)


def homepage(request):
    user=request.user.id
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



from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data   
            # {'username':'bikash', 'password':'subedi'} cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Login Success')
                
                if user.is_staff:
                    return redirect('/admins/')
                else:
                    
                    return redirect('/')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/login')


from django.contrib.auth.decorators import login_required
@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    check_items = Cart.objects.filter(user=user, product=product)
    if check_items:
        messages.add_message(request, messages.ERROR, 'Product is already added in cart')
        return redirect('/cartlist')
    else:
        Cart.objects.create(user=user, product=product)
        messages.add_message(request, messages.SUCCESS, 'Added product successfully in cart')
        return redirect('/cartlist')

@login_required    
def cart_list(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    data = {
        'items': items
    }
    return render(request, 'user/cart.html', data)


@login_required 
def orderitem(request, product_id, cart_id):
    user = request.user 
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(id=cart_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = int(request.POST.get('quantity'))
            price = product.product_price
            total_price = quantity * price
            contact_no = request.POST.get('contact_no')
            address = request.POST.get('address')
            email = request.POST.get('email')
            payment_method = request.POST.get('payment_method')

            order = Order.objects.create(
                product=product,
                user=user,
                quantity=quantity,
                total_price=total_price,
                contact_no=contact_no,
                address=address,
                email=email,
                payment_method=payment_method
            )
            
            if order.payment_method == "Cash on Delivery":
                cart.delete()
                messages.success(request, 'Order has been placed successfully. Be ready with cash.')
                return redirect('/cartlist')
            elif order.payment_method == "Esewa":
                # Redirect to Esewa payment gateway here
                return redirect(reverse('esewaform')+'?o_id='+str(order.id)+'&c_id='+str(cart.id))
            elif order.payment_method == "Khalti":
                # Redirect to Khalti payment gateway here
                pass
            else:
                messages.error(request, "Invalid payment option")
                return redirect('/cartlist')

    form = {
        'form': OrderForm()
    }
    return render(request, 'user/orderform.html', form)




@login_required
def orderlist(request):
    user = request.user
    order = Order.objects.filter(user=user)
    data = {
        'order': order
    }
    return render(request, 'user/myorder.html', data)


from django.shortcuts import get_object_or_404, redirect
@login_required
def delete_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item has been removed from the cart.')
    return redirect('/cartlist')



from django.views import View 

import hmac
import hashlib
import uuid
import base64
from django.shortcuts import render
from django.views import View
from product.models import Cart, Order  

class EsewaView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get('o_id')
        c_id = request.GET.get('c_id')
        cart = Cart.objects.get(id=c_id)
        order = Order.objects.get(id=o_id)

        uuid_val = uuid.uuid4()

        def genSha256(key, message):
            key = key.encode('utf-8')
            message = message.encode('utf-8')
            hmac_sha256 = hmac.new(key, message, hashlib.sha256)
            digest = hmac_sha256.digest()
            signature = base64.b64encode(digest).decode('utf-8')
            return signature

        secret_key = '8gBm/:&EnhH.1/q'
        data_to_sign = f"total_amount={order.total_price},transaction_uuid={uuid_val},product_code=EPAYTEST"
        result = genSha256(secret_key, data_to_sign)

        data = {
            'amount': order.product.product_price,
            'total_amount': order.total_price,
            'transaction_uuid': uuid_val,
            'product_code': 'EPAYTEST',
            'signature': result,
        }

        context = {
            'order': order,
            'data': data,
            'cart': cart
        }

        return render(request, 'user/esewa_payment.html', context)



import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
import base64

@login_required
def esewa_verify(request, order_id, cart_id):
    if request.method == 'GET':
        data = request.GET.get('data')
        decoded_data = base64.b64decode(data).decode('utf-8')
        map_data = json.loads(decoded_data)

        order = Order.objects.get(id=order_id)
        cart = Cart.objects.get(id=cart_id)

        if map_data.get('status') == 'COMPLETE':
            order.payment_status = True
            order.save()
            cart.delete()
            messages.add_message(request, messages.SUCCESS, 'Payment Successful')
            return redirect('/myorder')
        else:
            # Handle failed payment here if needed
            messages.add_message(request, messages.ERROR, 'Payment Failed')
            return redirect('/myorder')
