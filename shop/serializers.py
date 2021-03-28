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

    class Meta:
        model = ProductsOrders
        fields = ('order', 'product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True
    )
    status = serializers.ChoiceField(Order.OrderStatusChoices, default='NEW')
    order_products = ProductsOrdersSerializer(many=True)

    @staticmethod
    def create_new_products_orders(obj, data):
        for product in data:
            ProductsOrders.objects.create(order=obj, **product)
            obj.total += Product.objects.get(id=product.get('product').id).price * product.get('quantity')


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        products_data = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)

        self.create_new_products_orders(order, products_data)

        order.save()
        return order

    def update(self, order, validated_data):

        if 'order_products' in validated_data:
            products_data = validated_data.pop('order_products')

            if list(order.order_products.all()):
                for p in list(order.order_products.all()):
                    ProductsOrders.objects.get(order=order, product=p.product).delete()

            self.create_new_productsorders(order, products_data)

        order.status = validated_data.pop('status')
        order.save()
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
