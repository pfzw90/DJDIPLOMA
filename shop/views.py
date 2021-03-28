from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.viewsets import ModelViewSet
from shop.models import Product, Order, ProductReview, Collection
from shop.permissions import OnlyAdminCanEdit, OnlyOwnerCanEdit
from shop.serializers import ProductSerializer, OrderSerializer, ProductReviewSerializer, CollectionSerializer
from shop.filters import OrderFilter, ReviewFilter, ProductFilter


@permission_classes([OnlyAdminCanEdit, IsAuthenticated])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price']
    filterset_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [OnlyAdminCanEdit(), IsAuthenticated()]
        return []


@permission_classes([IsAuthenticated])
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderFilter
    ordering_fields = ['total', 'status']

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)


@permission_classes([IsAuthenticated, OnlyOwnerCanEdit])
class ReviewViewSet(ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    filterset_fields = ['user_id', 'created_at', 'id']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), OnlyOwnerCanEdit()]
        return []


@permission_classes([OnlyAdminCanEdit])
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            return [OnlyAdminCanEdit()]
        return []
