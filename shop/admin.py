from django.contrib import admin
from shop.models import Order, Product, ProductReview, Collection, ProductsOrders


admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(ProductsOrders)
admin.site.register(Collection)

