from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ModelViewSet
from shop.models import Product, Order, ProductReview, Collection
from shop.permissions import OnlyOwnerCanEdit, OnlyOwnerCanSee, OnlyAdminCanEdit
from shop.serializers import ProductSerializer, OrderSerializer, ProductReviewSerializer, CollectionSerializer
from shop.filters import OrderFilter, ReviewFilter, ProductFilter


@permission_classes([OnlyAdminCanEdit, AllowAny])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price']
    filterset_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [OnlyAdminCanEdit(), IsAuthenticated()]
        return []



@permission_classes([OnlyOwnerCanSee, IsAuthenticated])
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    filterset_fields = ['products', 'total', 'created_at', 'updated_at', 'status']

    def get_permissions(self):
        return [OnlyOwnerCanSee(), IsAuthenticated()]


@permission_classes([OnlyOwnerCanEdit, IsAuthenticated, AllowAny])
class ReviewViewSet(ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
    filterset_fields = ['user_id', 'created_at', 'id']

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [OnlyOwnerCanEdit(), IsAuthenticated()]
        return []



@permission_classes([OnlyAdminCanEdit, AllowAny])
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class=CollectionSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [OnlyAdminCanEdit()]
        return []
