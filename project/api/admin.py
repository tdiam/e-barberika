from django.contrib import admin

# Register your models here.
from .models import (
    Shop, ShopTag, Product, ProductTag, Price
)


admin.site.register(Shop)
admin.site.register(ShopTag)

admin.site.register(Product)
admin.site.register(ProductTag)

admin.site.register(Price)
