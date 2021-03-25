from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import serializers

from shop.models import Product, ProductReview, \
    Order, ProductsOrders, Collection


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=5000)
    price = serializers.DecimalField(max_digits=200, decimal_places=2)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price',
                  'created_at', 'updated_at')

    def validate(self, data):
        return data


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True
    )
    stars = serializers.ChoiceField(choices=ProductReview.ReviewStarsChoices)
    product_id = serializers.PrimaryKeyRelatedField

    class Meta:
        model = ProductReview
        fields = ('user', 'stars', 'product_id')

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        product_id = self.context['request'].data.get('product_id')

        if ProductReview.objects.filter(user=user, product_id=product_id):
            raise serializers.ValidationError("У Вас уже есть отзыв по данному товару")

        return data


class ProductsOrdersSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(source='order.id', read_only=True)
    product = serializers.PrimaryKeyRelatedField(source='product.id', read_only=True)
    quantity = serializers.IntegerField()

    class Meta:
        model = ProductsOrders
        fields = ('order', 'product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True
    )
    status = serializers.ChoiceField(Order.OrderStatusChoices, default='NEW')
    order_products = ProductsOrdersSerializer(many=True)

    def create(self, validated_data):
        print(validated_data)
        validated_data['user'] = self.context['request'].user
        validated_data['total'] = 0
        products_data = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            product = Product.objects.get(id=product_data.get('product'))
            quantity = product_data.get('quantity')
            ProductsOrders.objects.create(order=order, product=product, quantity=quantity)
            order.total += product.price * quantity
        return order

    def validate(self, data):
        request = self.context['request']
        if not request.user.is_staff and (request.data['status'] != 'NEW'):
            raise serializers.ValidationError('Менять статус заказа могут только администраторы')
        return data

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'order_products', 'total']


class CollectionSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(max_length=50)
    text = serializers.CharField(max_length=1000)
    products = ProductSerializer(many=True)

    class Meta:
        model = Collection
        fields = ('heading', 'text', 'products',
                  'created_at', 'updated_at')

    def validate(self, data):
        return data
