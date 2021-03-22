from django.contrib.auth.models import User
from rest_framework import serializers

from shop.models import Product, ProductReview, \
    Order, ProductsOrders, Collection, ReviewStarsChoices, OrderStatusChoices


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
        fields = ('id','name', 'description', 'price',
                  'created_at', 'updated_at')

    def validate(self, data):
        return data


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True
    )
    stars = serializers.ChoiceField(ReviewStarsChoices)
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
    order = serializers.ReadOnlyField(source='order.id')
    product = serializers.ReadOnlyField(source='product.id')
    quantity = serializers.IntegerField

    class Meta:
        model = ProductsOrders
        fields = ('order', 'product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        read_only=True
    )
    status = serializers.ChoiceField(OrderStatusChoices, default='NEW')
    products = ProductsOrdersSerializer(source='orders', many=True)

    def create(self, validated_data):
        validated_data["total"] = 0
        for p in self.context["request"].data.get('products'):
            validated_data["total"] += Product.objects.get(id=p.product).get['price'] * p.quantity

        return super().create(validated_data)

    def validate(self, data):
        request = self.context['request']
        if not request.user.get('is_admin') and (request.data.get('status') != 'NEW'):
            raise serializers.ValidationError('Менять статус заказа могут только администраторы')

    class Meta:
        model = Order
        fields = ('user', 'status', 'products', 'total')


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
