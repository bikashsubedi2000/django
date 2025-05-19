from django.urls import path
from . views import *

urlpatterns=[
    path('',adminhome,name='admins'),
    path('productlist/',productlist,name='productlist'),
    path('category/',categorylist,name='categorylist'),
    path('addproduct/',addproduct,name='addproduct'),
    path('addcategory/',addcategory,name='addcategory')
   
    
]