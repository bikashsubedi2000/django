import django_filters
from django_filters import CharFilter
from product.models import *

class ProductFilter(django_filters.FilterSet):
    product_name_contains = CharFilter(field_name='product_name', lookup_expr='icontains')
    
    class Meta:
        model = Product
        fields = ''
        exclude = ['product_price', 'description', 'quantity', 'image',
                   'category', 'create_at', 'uploaded_at']
