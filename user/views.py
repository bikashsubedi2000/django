from django.shortcuts import render,redirect
from product.models import *
from .filters import *

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate,login,logout
from .forms import *

from user.auth import *


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
                pass
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