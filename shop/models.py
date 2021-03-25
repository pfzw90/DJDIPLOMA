from django.db import models
from django.conf import settings


class Basic(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменен")

    class Meta:
        abstract = True


class Product(Basic):
    name = models.TextField(verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    price = models.IntegerField()

    def __str__(self):
        return self.name

class ProductReview(Basic):
    class ReviewStarsChoices(models.IntegerChoices):
        AWFUL = 1
        BAD = 2
        PASSABLY = 3
        GOOD = 4
        EXCELLENT = 5

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product_id = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=ReviewStarsChoices.choices, default=3, verbose_name='Оценка')
    text = models.TextField(max_length=5000)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product_id'], name='One review for each product')
        ]

    def __str__(self):
        return f'Отзыв пользователя {self.user} на товар \"{self.product_id.name}\"'

class Order(Basic):

    class OrderStatusChoices(models.TextChoices):
        NEW = "NEW", "Новый"
        IN_PROGRESS = "IN PROGRESS", "Выполняется"
        GONE = "FINISHED", "Завершен"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.TextField(choices=OrderStatusChoices.choices)
    total = models.DecimalField(max_digits=1000, decimal_places=2, editable=False)




class ProductsOrders(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False)


class Collection(Basic):
    heading = models.TextField(verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')
    products = models.ManyToManyField('Product', related_name='collections')

    def __str__(self):
        return f'{self.heading}'