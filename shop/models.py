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
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return self.name


class ProductReview(Basic):
    class ReviewStarsChoices(models.IntegerChoices):
        AWFUL = 1, "Ужасно"
        BAD = 2, "Плохо"
        PASSABLY = 3, "Нормально"
        GOOD = 4, "Хорошо"
        EXCELLENT = 5, "Отлично"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product_id = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE, verbose_name='Продукт')
    stars = models.IntegerField(choices=ReviewStarsChoices.choices, default=3, verbose_name='Оценка')
    text = models.TextField(max_length=5000, verbose_name='Текст отзыва')

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
        DONE = "FINISHED", "Завершен"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    status = models.TextField(choices=OrderStatusChoices.choices, verbose_name='Статус')
    total = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'Заказ №{self.id} от {self.created_at.strftime("%m/%d/%Y")}'


class ProductsOrders(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products',
                              blank=True, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(blank=False, verbose_name='Количество')


class Collection(Basic):
    heading = models.TextField(verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')
    products = models.ManyToManyField('Product', related_name='collections', verbose_name='Продукты')

    def __str__(self):
        return f'{self.heading}'
