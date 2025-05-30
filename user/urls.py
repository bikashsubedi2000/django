from django.urls import path
from .views import *
urlpatterns=[
    path('',homepage,name='homepage'),
    path('productpage/',productpage,name='productpage'),
    path('productdetail/<int:product_id>/', productdetail, name='productdetail'),
    path('register/',register,name="register"),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('addtocart/<int:product_id>',add_to_cart,name='addtocart'),
    path('cartlist/',cart_list,name='cartlist'),
    path('order/<int:product_id>/<int:cart_id>',orderitem,name='order'),
    path('myorder/',orderlist,name="myorder"),
    path('cart/delete/<int:cart_id>/', delete_cart_item, name='delete_cart_item'),
    # for esewa form 
    
    path('esewaform/',EsewaView.as_view(),name='esewaform'),
    path('esewaverify/<int:order_id>/<int:cart_id>', esewa_verify,name='esewaverify')  , 
    
]