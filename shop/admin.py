from django.contrib import admin
from shop.models import Order, Product, ProductReview, Collection


admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(Collection)

