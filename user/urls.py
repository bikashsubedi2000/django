from django.urls import path
from .views import *
urlpatterns=[
    path('',homepage,name='homepage'),
    path('productpage/',productpage,name='productpage'),
    path('productdetail/<int:product_id>/', productdetail, name='productdetail'),
    path('register/',register,name="register"),
    path('login/',login,name='login'),
    
]