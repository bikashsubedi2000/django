from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now=True, null=True)
    updated_at=models.DateTimeField(auto_now_add=True, null=True)
    
    
        
    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.IntegerField()
    description = models.TextField()
    quantity = models.IntegerField()
    image = models.FileField(upload_to='static/uploads',null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True, null=True)
    uploaded_at=models.DateTimeField(auto_now_add=True, null=True)
    
    
    def __str__ (self):
        return self.product_name
    

class Cart(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.user.username}"
    

class Order(models.Model):
    PAYMENT_METHOD = (
        ("Cash on Delivery", 'Cash on Delivery'),
        ("Esewa", "Esewa"),
        ("Khalti", "Khalti")
    )
    
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    total_price = models.IntegerField()
    quantity = models.IntegerField()
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=200)
    payment_status = models.CharField(default="Pending", max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=200)
    address = models.CharField(max_length=200)  
    email=models.EmailField()
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.product} - {self.payment_method}"  
    

