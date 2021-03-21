from django_filters import rest_framework as filters

from shop.models import Order, Collection, ProductReview, Product


class ProductFilter(filters.FilterSet):
    # name
    # description

    order = filters.OrderingFilter(
        fields=(
            ('price')
        )
    )

    class Meta:
        model = Product
        fields = ['price', 'name', 'description']


class ReviewFilter(filters.FilterSet):
    creator = filters.NumberFilter(field_name='user_id')
    id = filters.NumberFilter(field_name='id')
    created_at = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = ProductReview
        fields = ['user_id', 'created_at', 'id']



class OrderFilter(filters.FilterSet):

    #products

    total = filters.NumberFilter(field_name='total')
    status = filters.ChoiceFilter(field_name='status')
    created_at = filters.DateFromToRangeFilter(field_name='created_at')
    updated_at = filters.DateFromToRangeFilter(field_name='updated_at')


    class Meta:
        model = Order
        fields = ['products', 'total', 'created_at', 'updated_at', 'status']

