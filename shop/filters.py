import django_filters
from django_filters import fields
from django_filters import rest_framework as filters

from shop.models import Order, ProductReview, Product, ProductsOrders


class ProductFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'description']


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

    product_id = filters.ModelMultipleChoiceFilter(field_name='products', queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = ['products', 'total', 'created_at', 'updated_at', 'status', 'product_id']
