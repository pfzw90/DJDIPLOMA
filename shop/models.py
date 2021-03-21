from django.db import models
from django.conf import settings


class Basic(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ReviewStarsChoices(models.IntegerChoices):
    AWFUL = 1
    BAD = 2
    PASSABLY = 3
    GOOD = 4
    EXCELLENT = 5


class OrderStatusChoices(models.TextChoices):
    NEW = "NEW", "Новый"
    IN_PROGRESS = "IN PROGRESS", "Выполняется"
    GONE = "FINISHED", "Завершен"


class Product(Basic):
    name = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=200, decimal_places=2)


class ProductReview(Basic):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product_id = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=ReviewStarsChoices.choices, default=3)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product_id'], name='One review for each product')
        ]


class Order(Basic):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.TextField(choices=OrderStatusChoices.choices)
    total = models.DecimalField(max_digits=1000, decimal_places=2)
    products = models.ManyToManyField('Product', related_name='orders', through='ProductsOrders')


class ProductsOrders(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)


class Collection(Basic):
    heading = models.TextField
    text = models.TextField
    products = models.ManyToManyField('Product', related_name='collections')
