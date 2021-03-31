from urllib.parse import urlencode

from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html

from shop.models import Order, Product, ProductReview, Collection, ProductsOrders


class OrderForm(forms.ModelForm):
    def save(self, commit=True):
        order = super().save(commit=False)
        order.total = sum([Product.objects.get(id=product.product.id).price * product.quantity
                           for product in list(order.order_products.all())])
        return order


class ProductsOrdersInline(admin.TabularInline):
    model = ProductsOrders
    fields = ('product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at", "total", 'status', 'view_products')
    fields = ('user', 'total', 'status')
    readonly_fields = ['total']
    inlines = [ProductsOrdersInline]
    form=OrderForm

    def view_products(self, obj):
        display_text = format_html("</br>".join([
            "<a href=\"{}\">{}</a> - {} шт.".format(
                reverse('admin:shop_productsorders_change',
                        args=(product.pk,)),
                product.product, product.quantity)
            for product in obj.order_products.all()
        ]))
        if display_text:
            return display_text
        return format_html(f'<a href=\"{reverse("admin:shop_productsorders_add")}\">Добавить</a>')


admin.site.register(Product)


@admin.register(ProductsOrders)
class ProductsOrdersAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")


admin.site.register(ProductReview)
admin.site.register(Collection)
