import django_filters
from django_filters import rest_framework as filters

from shop.models import Order, ProductReview, Product, ProductsOrders


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['contains'],
            'description': ['contains']
        }


class ReviewFilter(filters.FilterSet):
    creator = filters.Filter(field_name='user_id')
    id = filters.NumberFilter(field_name='id')
    created_at = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = ProductReview
        fields = ['user_id', 'created_at', 'id']


class OrderFilter(filters.FilterSet):
    total = filters.RangeFilter(field_name='total')
    created_at = filters.DateFromToRangeFilter(field_name='created_at')
    updated_at = filters.DateFromToRangeFilter(field_name='updated_at')
    order_products = filters.ModelChoiceFilter(queryset=ProductsOrders.objects.all(), to_field_name='product_id')

    class Meta:
        model = Order
        fields = ['order_products', 'total', 'created_at', 'updated_at', 'status']
