from django.urls import path
from .views import *

urlpatterns = [
    path('product/',product,name='product'),
    path('',home,name='home'),
    path('category/',category,name='category'),

    
]