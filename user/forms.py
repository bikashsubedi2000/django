from django import forms
from django.forms import ModelForm
from product.models import *

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'payment_method', 'address', 'contact_no', 'email']
